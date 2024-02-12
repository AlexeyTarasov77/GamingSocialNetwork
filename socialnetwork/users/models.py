from django.db import models
from django.contrib.auth import get_user_model
from django.dispatch import receiver
from allauth.account.signals import user_signed_up
import os
from django.utils.text import slugify
from django.urls import reverse
from django.db.models.signals import post_save


# Create your models here.
def get_avatar_path(instance, filename):
    return os.path.join('photos', 'users', instance.user.username, filename)

    
class Profile(models.Model):
    user = models.OneToOneField(get_user_model(), related_name='profile_user', on_delete=models.CASCADE)
    user_slug = models.SlugField(verbose_name='URL профиля', unique=True, null=True, blank=True)
    is_online = models.BooleanField(default=False);
    image = models.ImageField(upload_to=get_avatar_path, blank=True, null=True)
    following = models.ManyToManyField(get_user_model(), related_name='profile_following', blank=True)
    followers = models.ManyToManyField(get_user_model(), related_name='profile_followers', blank=True)
    friends = models.ManyToManyField(get_user_model(), related_name='profile_friends', blank=True)
    bio = models.TextField(blank=True, null=True)
    date_of_birth = models.DateTimeField(null=True, blank=True)
    time_update = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        self.user_slug = slugify(self.user_slug)
    
    @property
    def get_profile_image(self):
        return self.image.url if self.image else '/static/users/images/profile.jpeg'
    
    def get_absolute_url(self):
        return reverse("users:profile", kwargs={"username": self.user_slug})
    

    
    
@receiver(user_signed_up, sender=get_user_model())
def create_user_profile(request, user, **kwargs):
    print('signal')
    print(Profile.objects.create(user=user))
