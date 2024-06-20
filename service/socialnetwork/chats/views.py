from django.db.models import Prefetch
from django.views import generic
from .models import ChatRoom, Message
from . import forms

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


class ChatRoomView(generic.DetailView, generic.FormView, ChatsMixin):
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
        context["chat_image"] = self.get_chat_image(chat)
        context["other_user"] = self.get_other_user(chat)
        return context
    
    def form_valid(self, form):
        msg = form.save(commit=False)
        msg.chat = self.object
        msg.author = self.request.user
        msg.save()
        return super().form_valid(form)