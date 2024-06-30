from chats.models import ChatRoom
from django.db.models import Q
from django.contrib.auth.models import AbstractBaseUser


class ChatsService:
    @staticmethod
    def get_other_user(chat: ChatRoom, curr_user_id: int) -> AbstractBaseUser | None:
        """
        Returns the user object of the other member in the chat room.
        """
        if not chat.is_group:
            return chat.members.exclude(id=curr_user_id).first()

    @classmethod
    def get_chat_image(cls, chat: ChatRoom) -> str:
        """
        Returns the URL of the image for the given chat room.
        For example to set chat image as avatar of other participant.
        """
        if chat.is_group:
            return chat.get_image()
        return cls.get_other_user(chat, chat.admin.id).profile.get_image()

    @staticmethod
    def is_chat_admin(user_id: int, chat: ChatRoom) -> bool:
        """Check whether the given user is admin of the given chat room."""
        return chat.admin_id == user_id

    @staticmethod
    def is_chat_member(user_id: int, chat: ChatRoom) -> bool:
        """Check whether the given user is member of the given chat room."""
        return chat.members.filter(id=user_id).exists()

    @staticmethod
    def generate_chat_name_by_members(members: list) -> str:
        return "&".join([member.username for member in members])  # joe&alex

    @staticmethod
    def is_unique_by_name(name: str) -> bool:
        return not ChatRoom.objects.filter(
            Q(name=name) | Q(name="&".join(list(reversed(name.split("&")))))  # joe&alex or alex&joe
        ).exists()
