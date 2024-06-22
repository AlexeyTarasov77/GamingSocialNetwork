from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings
import uuid

from django.urls import reverse

User = get_user_model()


# Create your models here.
class ChatRoom(models.Model):
    TYPE_CHOICES = (
        ("group", "Group"),
        ("personal", "Personal"),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, unique=True)
    image = models.ImageField(upload_to="photos/chat", null=True, blank=True)
    members = models.ManyToManyField(User, related_name="chats")
    admin = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="leading_chats"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=8, choices=TYPE_CHOICES, default=TYPE_CHOICES[0][0])

    class Meta:
        ordering = ["-created_at"]

    @property
    def is_group(self):
        return self.type == self.TYPE_CHOICES[0][0]

    def __str__(self) -> str:
        return self.name

    def get_image(self):
        return self.image.url if self.image else settings.DEFAULT_IMAGE_URL

    def get_absolute_url(self):
        return reverse("chats:detail", args=[self.id])


class Message(models.Model):
    STATUS_CHOICES = (
        ("read", "Read"),
        ("unread", "Unread"),
        ("deleted", "Deleted"),
    )
    chat = models.ForeignKey(
        ChatRoom, on_delete=models.CASCADE, related_name="messages"
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="chat_messages"
    )
    body = models.CharField(max_length=300)
    status = models.CharField(max_length=10, default=STATUS_CHOICES[1][0])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.body

    class Meta:
        ordering = ["-created_at"]
