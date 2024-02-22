from django.db import models
from django.contrib.auth import get_user_model
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
    online = models.IntegerField(default=0);
    image = models.ImageField(upload_to=get_avatar_path, blank=True, null=True, verbose_name="Фото профиля")
    bg_image = models.ImageField(upload_to=get_avatar_path, blank=True, null=True, verbose_name="Шапка профиля")
    following = models.ManyToManyField(get_user_model(), related_name='profile_following', blank=True)
    followers = models.ManyToManyField(get_user_model(), related_name='profile_followers', blank=True)
    friends = models.ManyToManyField(get_user_model(), related_name='profile_friends', blank=True)
    bio = models.TextField(blank=True, null=True, verbose_name="Биография")
    date_of_birth = models.DateTimeField(null=True, blank=True, verbose_name="Дата рождения")
    time_update = models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        return f'Профиль пользователя - {self.user}. Слаг - {self.user_slug}'
        
    def save(self, *args, **kwargs):
        self.user_slug = slugify(self.user.username)
        super(Profile, self).save(*args, **kwargs)
    
    @property
    def get_profile_image(self):
        return self.image.url if self.image else '/static/users/images/profile.jpeg'
    
    @property
    def get_background_image(self):
        return self.bg_image.url if self.bg_image else '/static/users/images/background.jpeg'
    
    def get_absolute_url(self):
        return reverse("users:profile", kwargs={"username": self.user_slug})
    