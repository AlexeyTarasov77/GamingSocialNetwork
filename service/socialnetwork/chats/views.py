from django.db.models import Prefetch
from django.views import generic
from django.views.generic.edit import FormMixin
from .models import ChatRoom, Message
from . import forms
generic.FormView

# Create your views here.

class ChatsMixin:
    def get_chat_image(self, chat):
        if chat.is_group:
            return chat.get_image()
        return self.get_other_user(chat).profile.get_image()

    def get_other_user(self, chat):
        if not chat.is_group:
            return chat.members.exclude(id=self.request.user.id).first()

class ListChatsView(generic.ListView, ChatsMixin):
    template_name = "chats/includes/list_chats.html"
    context_object_name = "chats"
    
    def get_queryset(self):
        qs = ChatRoom.objects.filter(members = self.request.user)
        self.chat_images = [self.get_chat_image(chat) for chat in qs]
        return qs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["zipped_chats"] = zip(self.get_queryset(), self.chat_images)
        return context


class ChatRoomView(generic.DetailView, FormMixin, ChatsMixin):
    template_name = "chats/chatroom.html"
    context_object_name = "chat"
    queryset = (
        ChatRoom.objects.all().prefetch_related(
            Prefetch('members'),
            Prefetch('messages', queryset=Message.objects.select_related('author__profile'))
        )
    )
    pk_url_kwarg = "chat_id"
    form_class = forms.MessageCreateForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        chat = self.object
        # raise Exception(self.get_chat_image(chat), self.get_other_user(chat), chat.is_group)
        print(self.get_chat_image(chat), self.get_other_user(chat), chat.is_group)
        context["chat_image"] = self.get_chat_image(chat)
        context["other_user"] = self.get_other_user(chat)
        return context