from django.urls import path, include
from . import views

app_name = 'chats'

urlpatterns = [
    path("", views.ListChatsView.as_view(), name="list"),
    path("<str:chat_id>/", views.ChatRoomView.as_view(), name="detail"),
]
