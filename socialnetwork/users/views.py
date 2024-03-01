from typing import Any
from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Profile, FriendRequest
from .forms import ProfileUpdateForm
from django.db.utils import ProgrammingError, OperationalError
from django.db import IntegrityError
from django.contrib import messages
from rest_framework import generics, status
from .serializers import SubscribeSerializer
from rest_framework.response import Response
from django.contrib.auth.models import User


# Create your views here.
class ProfileView(LoginRequiredMixin, generic.DetailView):
    template_name = "users/profile.html"
    context_object_name = "profile"

    def get_object(self, queryset: QuerySet[Any] | None = ...) -> Model:
        return get_object_or_404(Profile, user_slug=self.kwargs.get("username", None))

    def post(self, request, *args, **kwargs):
        if request.FILES["image"]:
            # try:
            print(request.FILES)
            instance = self.get_object()
            instance.image = request.FILES["image"]
            instance.save()
            return JsonResponse({"path": instance.image.url})
        # except [ProgrammingError, OperationalError, IntegrityError] as error:
        #     return JsonResponse({'error': error}, status=500)

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        profile = self.get_object()
        context["is_owner"] = (
            True if profile.user == self.request.user else False
        )
        context["request_exist"] = True if profile.requests.filter(from_user=self.request.user).exists() else False
        return context


def profile_middleware(request):
    if request.user.is_authenticated:
        return redirect(request.user.profile_user.get_absolute_url())
    else:
        return redirect("account_login")


class ProfileUpdateView(generic.UpdateView):
    slug_url_kwarg = "username"
    slug_field = "user_slug"
    template_name = "users/profile_update.html"
    model = Profile
    form_class = ProfileUpdateForm

    def form_valid(self, form):
        messages.success(self.request, "Профиль успешно обновлен")
        return super().form_valid(form)
    
def friend_requests_view(request, username):
    user = get_object_or_404(User, profile_user__user_slug=username)
    friend_requests = FriendRequest.objects.filter(to_user=user)
    print(friend_requests)
    return render(request, "users/friend_requests.html", {"friend_requests": friend_requests})


class SubscribeAPIView(generics.GenericAPIView):
    queryset = Profile.objects.all()
    # serializer_class = SubscribeSerializer
    lookup_field = "user_slug"
    lookup_url_kwarg = "username"

    # def get(self, request, username):
    #     user_profile = self.get_object()
    #     if request.user in user_profile.followers.all():
    #         return Response({"is_subscribed": True})
    #     else:
    #         return Response({"is_subscribed": False})

    def patch(self, request, username):
        user_profile = self.get_object()  # получение профиля пользователя на которого подписываются
        user = request.user  # получение текущего пользователя который хочеть подписаться/отписаться
        if user in user_profile.followers.all():  # если пользователь уже подписан
            user_profile.followers.remove(user)  # отписаться
            user.profile_user.following.remove(user_profile.user)  # удалить из подписок пользователя от которого отписываемся
            return Response({"is_subscribed": False})
        else:  # если пользователь еще не подписан
            user_profile.followers.add(request.user)  # подписаться
            user.profile_user.following.add(user_profile.user) # добавить в подписки пользователя на которого подписываемся
            return Response({"is_subscribed": True})
        
class FriendRequestAPIView(generics.GenericAPIView):
    queryset = Profile.objects.all()
    lookup_field = "user_slug"
    lookup_url_kwarg = "username"
        
    def post(self, request, username):
        """Создание заявки в друзья"""
        profile = self.get_object()
        data = {"from_user": request.user, "to_user": profile.user, "to_profile": profile}
        FriendRequest.objects.create(**data)
        
        return Response({"sent": True}, status=status.HTTP_201_CREATED)
        
    def delete(self, request, username):
        """Удаление из друзей"""
        user_profile1 = self.get_object()
        user1 = self.get_object().user
        user_profile2 = get_object_or_404(Profile, user=request.user)
        user2 = request.user
        action = request.data["action"]
        msg = ''
        if action == 'delete':
            user_profile1.friends.remove(user2)
            user_profile2.friends.remove(user1)
            msg = 'Удален из друзей'
        elif action == 'cancel':
            FriendRequest.objects.get(from_user=user2, to_user=user1).delete()
            msg='Заявка в друзья отменена'
        return Response({"removed": True, "msg": msg}, status=status.HTTP_204_NO_CONTENT)
        
        
class FriendRequestHandlerAPIView(generics.GenericAPIView):
    queryset = Profile.objects.all()
    lookup_field = "user_slug"
    lookup_url_kwarg = "username"
    
    def post(self, request, username):
        """Принятие заявки в друзья"""
        user_profile1 = self.get_object()
        user_profile2 = get_object_or_404(Profile, user__pk=request.data["user_pk"])
        user_profile1.friends.add(user_profile2.user)
        user_profile2.friends.add(user_profile1.user)
        FriendRequest.objects.get(from_user=user_profile1.user, to_user=user_profile2.user).delete()
        return Response({"accepted": True}, status=status.HTTP_201_CREATED)
        
        
    def delete(self, request, username):
        """Отклонение заявки в друзья"""
        user1 = self.get_object().user
        user2 = get_object_or_404(User, pk=request.data["user_pk"])
        FriendRequest.objects.get(from_user=user1, to_user=user2).delete()
        return Response({"accepted": False}, status=status.HTTP_201_CREATED)
        
        

