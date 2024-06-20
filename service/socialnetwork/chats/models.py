from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings
import uuid

User = get_user_model()

# Create your models here.
class ChatRoom(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, unique=True)
    image = models.ImageField(upload_to='photos/chat', null=True, blank=True)
    members = models.ManyToManyField(User, related_name='rooms')
    admin = models.ForeignKey(User, on_delete=models.CASCADE, related_name='leading_rooms')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name
    
    @property
    def is_group(self):
        return self.members.count() > 2
    
    def get_image(self):
        return self.image.url if self.image else settings.DEFAULT_IMAGE_URL
    
    
class Message(models.Model):
    STATUS_CHOICES = (
        ('read', 'Read'),
        ('unread', 'Unread'),
        ('deleted', 'Deleted'),
    )
    chat = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_messages')
    body = models.TextField(max_length=300)
    status = models.CharField(max_length=10, default=STATUS_CHOICES[1][0])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.body
    
    class Meta:
        ordering = ['-created_at']
    