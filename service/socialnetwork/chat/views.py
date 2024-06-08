from django.shortcuts import render

# Create your views here.

def list_rooms_view(request):
    ...

def room_view(request, room_name):
    return render(request, 'chat/room.html', {
        'room_name': room_name
    })