import logging
from typing import Any

from core.redis_connection import r
from core.views import CatchExceptionMixin, catch_exception, set_logger
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views import generic
from posts.models import Post
from rest_framework import generics, status
from rest_framework.response import Response

from .decorators import owner_required
from .forms import ProfileUpdateForm
from .models import FriendRequest, Profile

logger = logging.getLogger(__name__)
set_logger(logger)


class ProfileView(CatchExceptionMixin, LoginRequiredMixin, generic.DetailView):
    """View for user's profile page"""

    template_name = "users/profile.html"
    context_object_name = "profile"
    queryset = Profile.objects.select_related("user").prefetch_related(
        "following", "followers", "friends"
    )
    slug_url_kwarg = "username"
    slug_field = "user_slug"

    def post(self, request, *args, **kwargs):
        """Updating profile image."""
        if request.FILES["image"]:
            instance = self.object
            instance.image = request.FILES["image"]
            instance.save()
            return JsonResponse({"path": instance.image.url})

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """
        Passing to context additional params:
            is_owner: is current user a profile owner or he've just visited it as guest.
            request_exist: did current user send a friend request to this profile.
            is_online: is profile's owner online or not.
        """
        context = super().get_context_data(**kwargs)
        profile = self.object
        context["is_owner"] = True if profile.user == self.request.user else False
        # отправлял ли текущий пользователь запрос в друзья
        context["request_exist"] = (
            True if profile.requests.filter(from_user=self.request.user).exists() else False
        )
        context["is_online"] = int(r.get(f"user:{profile.user.id}:status") or 0) > 0

        return context


@catch_exception
@owner_required("users")
def my_posts_view(request, username):
    """View posts of current user"""
    user = get_object_or_404(
        User,
        profile__user_slug=username,
    )
    context = {
        "own_posts": user.posts.all(),
        "liked_posts": user.liked_posts.all(),
        "saved_posts": user.saved_posts.all(),
        "drafts_posts": Post.objects.filter(author=user, status="DF"),
        "is_owner": True if user == request.user else False,
    }
    return render(request, "users/my_posts.html", context)


@catch_exception
@owner_required("users")
def my_orders_view(request, username):
    """View orders of current user"""
    user = get_object_or_404(
        User.objects.select_related("profile").prefetch_related("orders"),
        profile__user_slug=username,
    )
    context = {"orders": user.orders.all()}
    return render(request, "users/my_orders.html", context)


@catch_exception
def profile_middleware(request):
    if request.user.is_authenticated:
        return redirect(request.user.profile.get_absolute_url())
    else:
        return redirect("account_login")


class ProfileUpdateView(CatchExceptionMixin, generic.UpdateView):
    """View for updating profile."""

    slug_url_kwarg = "username"
    slug_field = "user_slug"
    template_name = "users/profile_update.html"
    model = Profile
    form_class = ProfileUpdateForm

    def form_valid(self, form):
        messages.success(self.request, "Профиль успешно обновлен")
        return super().form_valid(form)


@catch_exception
def friend_requests_view(request, username):
    """View all incoming friend requests to current user."""
    user = get_object_or_404(User, profile_user__user_slug=username)
    friend_requests = FriendRequest.objects.filter(to_user=user)
    print(friend_requests)
    return render(request, "users/friend_requests.html", {"friend_requests": friend_requests})


class SubscribeAPIView(CatchExceptionMixin, generics.GenericAPIView):
    """Api view for subscribe/unsubscribe to user"""

    queryset = Profile.objects.all()
    lookup_field = "user_slug"
    lookup_url_kwarg = "username"

    def patch(self, request, username):
        target_user_profile = (
            self.get_object()
        )  # получение профиля пользователя на которого подписываются
        acting_user = (
            request.user
        )  # получение текущего пользователя который хочеть подписаться/отписаться
        if acting_user in target_user_profile.followers.all():  # если пользователь уже подписан
            target_user_profile.followers.remove(acting_user)  # отписаться
            acting_user.profile.following.remove(
                target_user_profile.user
            )  # удалить из подписок пользователя от которого отписываемся
            return Response({"is_subscribed": False})
        else:  # если пользователь еще не подписан
            target_user_profile.followers.add(request.user)  # подписаться
            acting_user.profile.following.add(
                target_user_profile.user
            )  # добавить в подписки пользователя на которого подписываемся
            return Response({"is_subscribed": True})


@catch_exception
def friend_request_remove(from_user: User, to_user: User) -> None:
    """Удаление заявки в друзья"""
    FriendRequest.objects.get(from_user=from_user, to_user=to_user).delete()


class FriendRequestAPIView(CatchExceptionMixin, generics.GenericAPIView):
    """View for managing friend requests based on request method."""

    queryset = Profile.objects.all()
    lookup_field = "user_slug"
    lookup_url_kwarg = "username"

    def post(self, request, username):
        """Создание заявки в друзья"""
        profile = self.get_object()  # профиль пользователя которому отправляют заявку
        data = {
            "from_user": request.user,
            "to_user": profile.user,
            "to_profile": profile,
        }  # формирование данных для создания заявки
        FriendRequest.objects.create(**data)

        return Response({"sent": True}, status=status.HTTP_201_CREATED)

    def delete(self, request, username):
        """Удаление из друзей или отмена заявки"""
        user_profile1 = self.get_object()  # получение профиля пользователя которому отправляли заявку
        user1 = self.get_object().user  # получение юзера из профиля пользователя
        user_profile2 = get_object_or_404(
            Profile, user=request.user
        )  # получение профиля пользователя который отправил заявку (или хочеть удалить из друзей)
        user2 = request.user  # соответствующий юзер
        action = request.data[
            "action"
        ]  # действие которое надо выполнить (либо удаление заявки либо отмена отправки)
        msg = ""  # инициализация сообщения для возврата на клиент в зависимости от выполненного действия
        if action == "delete":
            # если действие - удалить из друзей, взаимоудаляем
            user_profile1.friends.remove(user2)
            user_profile2.friends.remove(user1)
            msg = "Удален из друзей"
        elif action == "cancel":
            # если пользователь хочет отменить заявку просто удаляем ее у соответствующего пользователя
            friend_request_remove(user2, user1)
            msg = "Заявка в друзья отменена"
        return Response({"removed": True, "msg": msg}, status=status.HTTP_204_NO_CONTENT)


class FriendRequestHandlerAPIView(CatchExceptionMixin, generics.GenericAPIView):
    """View for declining/accepting friend request"""

    queryset = Profile.objects.all()
    lookup_field = "user_slug"
    lookup_url_kwarg = "username"

    def post(self, request, username):
        """Принятие заявки в друзья"""
        user_profile1 = self.get_object()  # получение профиля пользователя который принимает заявку
        user_profile2 = get_object_or_404(
            Profile, user__pk=request.data["user_pk"]
        )  # получение профиля пользователя которому принадлежит заявка
        # взаимодобавление в друзья к друг другу
        user_profile1.friends.add(user_profile2.user)
        user_profile2.friends.add(user_profile1.user)
        # удаление заявки
        friend_request_remove(user_profile2.user, user_profile1.user)
        return Response({"accepted": True}, status=status.HTTP_201_CREATED)

    def delete(self, request, username):
        """Отклонение заявки в друзья"""
        user1 = (
            self.get_object().user
        )  # получение юзера из профиля пользователя который отклоняет заявку
        user2 = get_object_or_404(
            User, pk=request.data["user_pk"]
        )  # юзер который отправил заявку (чья заявка отклоняеться)
        friend_request_remove(user2, user1)  # удаление заявки
        return Response({"accepted": False}, status=status.HTTP_204_NO_CONTENT)
