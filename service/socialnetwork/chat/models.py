from django.db import models
from django.contrib.auth import get_user_model
import uuid

User = get_user_model()

# Create your models here.
class Chat(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    participants = models.ManyToManyField(User, related_name='rooms')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    
class Message(models.Model):
    STATUS_CHOICES = (
        ('read', 'Read'),
        ('unread', 'Unread'),
        ('deleted', 'Deleted'),
    )
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    status = models.CharField(max_length=10, default=STATUS_CHOICES[1][0])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content
    