from django.db import models
from django.contrib.auth import get_user_model
import os


# Create your models here.
def get_avatar_path(instance, filename):
    return os.path.join('photos', 'users', instance.username, filename)

    
class Profile(models.Model):
    user = models.OneToOneField(get_user_model(), related_name='profile_user', on_delete=models.CASCADE)
    is_online = models.BooleanField(default=False);
    image = models.ImageField(upload_to=get_avatar_path, blank=True, null=True)
    following = models.ManyToManyField(get_user_model(), related_name='profile_following', blank=True)
    friends = models.ManyToManyField(get_user_model(), related_name='profile_friends', blank=True)
    bio = models.TextField(blank=True, null=True)
    date_of_birth = models.DateTimeField(null=True, blank=True)
    time_update = models.DateTimeField(auto_now=True)