from typing import Any
from django.db.models import Prefetch
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.views import generic
from django.views.generic.edit import FormMixin, BaseFormView
from django.contrib.auth.mixins import AccessMixin, LoginRequiredMixin
from django.contrib import messages
from django.db.models import Q
from users.services.users_service import UsersService
from .services.chats_service import ChatsService
from chats import forms
from .models import ChatRoom, Message
from core.utils import is_ajax

# Create your views here.


class ChatsMixin:
    """
    Mixin for views that interact with chat rooms.
    """

    def get_chat_image(self, chat):
        return ChatsService.get_chat_image(chat)

    def get_other_user(self, chat):
        return ChatsService.get_other_user(chat, self.request.user.id)


class ChatAccessMixin(AccessMixin):
    """
    Mixin for views that require access to chat rooms.
    """

    permission_denied_message = "You do not have permission to access this chat room."

    def test_user_func(self):
        raise NotImplementedError

    def dispatch(self, request, *args, **kwargs):
        """Checks if the user has access to the chat room."""
        print('calling dispatch')
        if not self.request.user.is_authenticated or not self.test_user_func():
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class MemberRequiredMixin(ChatAccessMixin):
    """Check if current user is a member of accessing chat room."""
    def test_user_func(self):
        return ChatsService.is_chat_member(self.request.user.id, self.get_object())


class AdminRequiredMixin(ChatAccessMixin):
    """Check if current user is an admin of accessing chat room."""
    def test_user_func(self):
        return ChatsService.is_chat_admin(self.request.user.id, self.get_object())


class ListChatsView(LoginRequiredMixin, generic.ListView, ChatsMixin):
    """
    View for displaying a list of chat rooms.
    """

    template_name = "chats/includes/list_chats_sidebar.html"
    context_object_name = "chats"

    def get_queryset(self):
        """
        Retrieve the queryset of chat rooms for the current user.
        Creates a list of images for each chat room.
        Returns:
            QuerySet: The queryset of chat rooms.
        """
        qs = ChatRoom.objects.filter(members=self.request.user)
        self.chat_images = [self.get_chat_image(chat) for chat in qs]
        return qs

    def get_template_names(self) -> list[str]:
        if is_ajax(self.request):
            return super().get_template_names()
        return ["chats/list_chats.html"]

    def get_context_data(self, **kwargs):
        """
        Adds to context chats zipped with their computed images.
        """
        context = super().get_context_data(**kwargs)
        context["zipped_chats"] = zip(self.get_queryset(), self.chat_images)
        return context


class ChatRoomView(ChatsMixin, MemberRequiredMixin, generic.DetailView, FormMixin):
    """View for displaying a chat room and handling form submissions."""

    template_name = "chats/chatroom.html"
    context_object_name = "chat"
    queryset = ChatRoom.objects.all().prefetch_related(
        Prefetch("members"),
        Prefetch(
            "messages", queryset=Message.objects.select_related("author__profile")
        ),
    )
    pk_url_kwarg = "chat_id"
    form_class = forms.MessageCreateForm

    def get_template_names(self) -> list[str]:
        """
        Determine the template to use based on the request headers.

        Returns:
            list[str]: The names of the templates to use.
        """
        if is_ajax(self.request):
            return ["chats/partials/chatroom_p.html"]
        return super().get_template_names()

    def get_context_data(self, **kwargs):
        """
        Get the context data for rendering the template.
        Adding the chat image and the other user to the context.
        """
        context = super().get_context_data(**kwargs)
        chat = self.object
        print(self.get_chat_image(chat), self.get_other_user(chat), chat.is_group)
        context["chat_image"] = self.get_chat_image(chat)
        context["other_user"] = self.get_other_user(chat)
        return context

    def form_valid(self, form: forms.MessageCreateForm) -> HttpResponse:
        """
        Saving messages is done in the websockets.
        This method uses in case when websockets not supported or not available right now.
        """
        msg = form.save(commit=False)
        msg.author = self.request.user
        msg.chat = self.object
        msg.save()
        return super().form_valid(form)


class GroupChatRoomCreateView(LoginRequiredMixin, generic.CreateView):
    """
    View for creating a new group chat room.
    """

    template_name = "chats/chatroom_create.html"
    form_class = forms.GroupChatRoomCreateForm

    def get_form_kwargs(self) -> dict[str, Any]:
        """Puts suggested users for choosing to add in group to the form kwargs."""
        kwargs = super().get_form_kwargs()
        suggested_users = UsersService.get_suggested_users_per_user(self.request.user)
        kwargs.update(
            members_queryset=suggested_users,
        )
        return kwargs

    def form_valid(self, form: forms.GroupChatRoomCreateForm) -> HttpResponse:
        """
        Save the form data and add additional data.
        """
        chat = form.save(commit=False)
        user = self.request.user
        chat.admin = user
        chat.save()
        chat.members.add(user, *form.cleaned_data["members"])
        chat.save()
        return HttpResponse(chat.get_absolute_url())


class PersonalChatRoomCreateView(LoginRequiredMixin, BaseFormView):
    """
    View for creating a new personal chat room.
    """

    form_class = forms.PersonalChatRoomCreateForm

    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        return HttpResponse(status=402)  # not allowed

    def form_invalid(self, form):
        print(form.errors)
        return HttpResponse(form.errors, status=400)

    def form_valid(self, form: forms.PersonalChatRoomCreateForm) -> HttpResponse:
        chat = form.save(commit=False)
        chat_members = form.cleaned_data["members"]
        chat.name = ChatsService.generate_chat_name_by_members(chat_members)
        if ChatsService.is_unique_by_name(chat.name):
            chat.admin = self.request.user
            chat.type = ChatRoom.TYPE_CHOICES[1][0]  # personal
            chat.save()
            form.save_m2m()
        return redirect(chat.get_absolute_url())


class ChatRoomMemberRemoveView(
    generic.detail.SingleObjectMixin,
    generic.View,
    MemberRequiredMixin
):
    """
    View for removing member from chat room.
    Member can leave chat his self or chat's admin can remove him.
    """
    pk_url_kwarg = "chat_id"
    model = ChatRoom

    def get_success_msg(self, target_user_id, curr_user_id) -> str:
        """Determines the success message for removing member from chat room."""
        msg = ''
        if target_user_id == curr_user_id:
            msg = "Вы покинули чат"
        else:
            msg = "Пользователь удален из чата"
        return msg

    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        response = redirect("chats:list")
        chat = self.get_object()
        target_user_id = int(request.POST.get("target_user_id"))  # user that we want to remove
        curr_user_id = request.user.id
        #  alias for func
        is_admin = lambda user_id: ChatsService.is_chat_admin(user_id, chat)  # noqa
        print(target_user_id, (target_user_id not in chat.members.all()))
        if not target_user_id or not ChatsService.is_chat_member(target_user_id, chat):
            return HttpResponse(status=400)
        #  user leaves team
        if target_user_id == curr_user_id:
            chat.members.remove(target_user_id)
        #  user wants to remove another user
        else:
            # if user want to remove another user and isn't chat's admin - forbidden
            if not is_admin(curr_user_id):
                return HttpResponse(status=403)
            #  admin kick another user
            chat.members.remove(target_user_id)
            response = JsonResponse({"success": True, "data": {"removed_user_id": target_user_id}})
        # if after removing memeber nobody left or removed member was admin - delete chat
        if chat.members.count() == 0 or is_admin(target_user_id):
            chat.delete()
            response = redirect("chats:list")
        #  add msg only in case that response is http (not json)
        if type(response) is HttpResponse:
            messages.success(request, self.get_success_msg(target_user_id, curr_user_id))
        return response
