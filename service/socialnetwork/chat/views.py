from django.shortcuts import render
from django.views import generic
from .models import ChatRoom

# Create your views here.

def list_rooms_view(request):
    ...

def room_view(request, room_name):
    return render(request, 'chat/room.html', {
        'room_name': room_name
    })
    
    
class ListChatsView(generic.ListView):
    template_name = 'chat/list_chats.html'
    context_object_name = 'chats'
    queryset = ChatRoom.objects.all()
    
    
class ChatRoomView(generic.DetailView):
    template_name = 'chat/room.html'
    context_object_name = 'room'
    queryset = ChatRoom.objects.all().prefetch_related('messages')
    pk_url_kwarg = 'chat_id'
    
    
