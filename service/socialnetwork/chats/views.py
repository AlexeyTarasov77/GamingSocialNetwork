from typing import Any
from django.db.models import Prefetch
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.views import generic
from django.views.generic.edit import FormMixin, BaseFormView
from django.db.models import Q
from posts.services.PostList import PostSuggestionService
from . import forms
from .models import ChatRoom, Message

# Create your views here.


class ChatsMixin:
    """
    Mixin for views that interact with chat rooms.

    Attributes:
        None

    Methods:
        get_chat_image(chat)
            Returns the URL of the image for the given chat room.

        get_other_user(chat)
            Returns the user object of the other member in the chat room.
    """

    def get_chat_image(self, chat):
        """
        Returns the URL of the image for the given chat room.

        Args:
            chat (ChatRoom): The chat room object.

        Returns:
            str: The URL of the image for the chat room.
        """
        if chat.is_group:
            return chat.get_image()
        return self.get_other_user(chat).profile.get_image()

    def get_other_user(self, chat):
        """
        Returns the user object of the other member in the chat room.

        Args:
            chat (ChatRoom): The chat room object.

        Returns:
            User: The user object of the other member in the chat room.
        """
        if not chat.is_group:
            return chat.members.exclude(id=self.request.user.id).first()


class ListChatsView(generic.ListView, ChatsMixin):
    """
    View for displaying a list of chat rooms.

    Attributes:
        template_name (str): The name of the template to use for rendering.
        context_object_name (str): The name of the context variable to use
        for the chat rooms list.
        queryset (QuerySet): The queryset of chat rooms to retrieve.
        chat_images (List[str]): The list of images for each chat room.

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
        if self.request.headers.get("Hx-Request") == "true":
            return super().get_template_names()
        return ["chats/list_chats.html"]

    def get_context_data(self, **kwargs):
        """
        Get the context data for rendering the template.
        Adding `zipped_chats` to the context for iterating over the chat rooms
        and their images.
        """
        context = super().get_context_data(**kwargs)
        context["zipped_chats"] = zip(self.get_queryset(), self.chat_images)
        return context


class ChatRoomView(generic.DetailView, FormMixin, ChatsMixin):
    """
    View for displaying a chat room and handling form submissions.

    Attributes:
        template_name (str): The name of the template to use for rendering.
        context_object_name (str): The name of the context variable to use
        for the chat room object.
        queryset (QuerySet): The queryset of chat rooms to retrieve.
        pk_url_kwarg (str): The URL kwarg to use for the chat room ID.
        form_class (type): The form class to use for creating messages.
    """

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
        print("HEADERS", self.request.headers)
        if self.request.headers.get("Hx-Request") == "true":
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
        Save the form data and associate it with the current user and chat.

        Args:
            form (forms.MessageCreateForm): The form containing the message data.

        Returns:
            HttpResponse: The response after the form is successfully saved.
        """
        msg = form.save(commit=False)
        msg.author = self.request.user
        msg.chat = self.object
        msg.save()
        return super().form_valid(form)


class GroupChatRoomCreateView(generic.CreateView):
    """
    View for creating a new chat room.

    Attributes:
        template_name (str): The name of the template to use for rendering.
        form_class (type): The form class to use for creating chat rooms.
    """

    template_name = "chats/chatroom_create.html"
    form_class = forms.GroupChatRoomCreateForm

    def get_form_kwargs(self) -> dict[str, Any]:
        kwargs = super().get_form_kwargs()
        suggestion_service = PostSuggestionService()
        kwargs.update(members_queryset=suggestion_service.get_suggested_users(self.request.user))

    def form_valid(self, form: forms.GroupChatRoomCreateForm) -> HttpResponse:
        """
        Save the form data and associate it with the current user.
        """
        chat = form.save(commit=False)
        chat.admin = self.request.user
        chat.save()
        chat.members.add(self.request.user)
        form.save_m2m()
        return redirect(chat.get_absolute_url())


class PersonalChatRoomCreateView(BaseFormView):
    form_class = forms.PersonalChatRoomCreateForm

    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        return HttpResponse(status=402)  # not allowed

    def form_invalid(self, form):
        print(form.errors)
        return HttpResponse(form.errors, status=400)

    def form_valid(self, form: forms.PersonalChatRoomCreateForm) -> HttpResponse:
        chat = form.save(commit=False)
        chat_members = form.cleaned_data["members"]
        chat.name = "&".join(
            [member.username for member in chat_members]
        )  # joe&alex
        if not ChatRoom.objects.filter(
            Q(name=chat.name) | Q(name="&".join(list(reversed("joe&alex".split("&")))))
        ).exists():  # joe&alex or alex&joe
            chat.admin = self.request.user
            chat.type = ChatRoom.TYPE_CHOICES[1][0]  # personal
            chat.save()
            form.save_m2m()
        return redirect(chat.get_absolute_url())
