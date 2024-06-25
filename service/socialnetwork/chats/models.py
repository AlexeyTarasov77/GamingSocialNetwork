from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _
from django.conf import settings
import uuid

from django.urls import reverse

User = get_user_model()


# Create your models here.
class ChatRoom(models.Model):
    """
    Model representing a chat room.

    Attributes:
        id (UUIDField): The unique identifier of the chat room.
        name (CharField): The name of the chat room.
        image (ImageField): The image of the chat room.
        members (ManyToManyField): The members of the chat room.
        admin (ForeignKey): The admin of the chat room.
        created_at (DateTimeField): The creation date of the chat room.
        type (CharField): The type of the chat room.

    Meta:
        ordering: The ordering of the chat rooms.
    """

    TYPE_CHOICES = (
        ("group", "Group"),
        ("personal", "Personal"),
    )
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, verbose_name=_("ID")
    )
    name = models.CharField(max_length=255, unique=True, verbose_name=_("name"))
    image = models.ImageField(
        upload_to="photos/chat", null=True, blank=True, verbose_name=_("image")
    )
    members = models.ManyToManyField(
        User, related_name="chats", verbose_name=_("members")
    )
    admin = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="leading_chats",
        verbose_name=_("admin"),
    )
    created_at = models.DateTimeField(
        auto_now_add=True, db_index=True, verbose_name=_("created at")
    )
    type = models.CharField(
        max_length=8,
        choices=TYPE_CHOICES,
        default=TYPE_CHOICES[0][0],
        verbose_name=_("type"),
    )

    class Meta:
        ordering = ["-created_at"]

    @property
    def is_group(self) -> bool:
        """
        Check if the chat room is a group chat by comparing chatroom type with group type.
        """
        return self.type == self.TYPE_CHOICES[0][0]

    def __str__(self) -> str:
        return self.name

    def get_image(self) -> str:
        """
        Get the URL of the chat room image.
        """
        return self.image.url if self.image else settings.DEFAULT_IMAGE_URL

    def get_absolute_url(self) -> str:
        """
        Get the absolute URL for the chat room detail page.
        """
        return reverse("chats:detail", args=[self.id])


class Message(models.Model):
    """
    Model class for storing messages in chat rooms.

    Attributes:
        chat (ForeignKey): Foreign key to ChatRoom model.
        author (ForeignKey): Foreign key to User model.
        body (CharField): Text content of the message.
        status (CharField): Status of the message.
        created_at (DateTimeField): Time when the message was created.
    """

    STATUS_CHOICES = (
        ("read", "Read"),
        ("unread", "Unread"),
        ("deleted", "Deleted"),
    )
    chat = models.ForeignKey(
        ChatRoom,
        on_delete=models.CASCADE,
        related_name="messages",
        verbose_name=_("chat"),
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="chat_messages",
        verbose_name=_("author"),
    )
    body = models.CharField(max_length=300, verbose_name=_("body"))
    status = models.CharField(
        max_length=10,
        default=STATUS_CHOICES[1][0],
        choices=STATUS_CHOICES,
        verbose_name=_("status"),
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("created at"))

    def __str__(self) -> str:
        return self.body

    class Meta:
        ordering = ["-created_at"]
