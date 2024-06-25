from django.urls import path
from . import views

app_name = "chats"

urlpatterns = [
    path("", views.ListChatsView.as_view(), name="list"),
    path("<uuid:chat_id>/", views.ChatRoomView.as_view(), name="detail"),
    path(
        "create-personal/",
        views.PersonalChatRoomCreateView.as_view(),
        name="create-personal",
    ),
    path("create-group/", views.GroupChatRoomCreateView.as_view(), name="create-group"),
    path(
        "remove-member-from/<uuid:chat_id>/",
        views.ChatRoomMemberRemoveView.as_view(),
        name="remove-member",
    ),
]
