import os

from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext as _
from django_countries.fields import CountryField
from gameblog.mixins import SaveSlugMixin


# Create your models here.
def get_avatar_path(instance, filename):
    return os.path.join("photos", "users", instance.user.username, filename)


class Profile(SaveSlugMixin, models.Model):
    user = models.OneToOneField(
        get_user_model(),
        related_name="profile",
        on_delete=models.CASCADE,
        verbose_name=_("Пользователь"),
    )
    user_slug = models.SlugField(
        verbose_name="URL профиля", unique=True, null=True, blank=True
    )
    image = models.ImageField(
        upload_to=get_avatar_path, blank=True, null=True, verbose_name=_("Фото профиля")
    )
    bg_image = models.ImageField(
        upload_to=get_avatar_path,
        blank=True,
        null=True,
        verbose_name=_("Шапка профиля"),
    )
    following = models.ManyToManyField(
        get_user_model(),
        related_name="profile_following",
        blank=True,
        verbose_name=_("Подписки"),
    )
    followers = models.ManyToManyField(
        get_user_model(),
        related_name="profile_followers",
        blank=True,
        verbose_name=_("Подписчики"),
    )
    friends = models.ManyToManyField(
        get_user_model(),
        related_name="profile_friends",
        blank=True,
        verbose_name=_("Друзья"),
    )
    bio = models.TextField(blank=True, null=True, verbose_name=_("Биография"))
    date_of_birth = models.DateTimeField(
        null=True, blank=True, verbose_name=_("Дата рождения")
    )
    country = CountryField(blank=True, null=True, verbose_name=_("Страна"))
    team = models.ForeignKey(
        "gameteams.Team",
        verbose_name=_("Команда"),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="members",
    )
    time_update = models.DateTimeField(auto_now=True, verbose_name=_("Дата обновления"))

    def __str__(self) -> str:
        return f"Профиль пользователя - {self.user}."

    @property
    def is_leader(self):
        if self.team:
            return self.team.leader == self.user
        return False

    @property
    def age(self):
        if self.date_of_birth:
            return (timezone.now() - self.date_of_birth).days // 365

    def save(self, *args, **kwargs):
        return super().save(
            *args, slug_field="user_slug", slugify_value=self.user.username, **kwargs
        )

    def get_profile_image(self):
        return self.image.url if self.image else "/static/users/images/profile.jpeg"

    def get_background_image(self):
        return (
            self.bg_image.url
            if self.bg_image
            else "/static/users/images/background.jpeg"
        )

    def get_absolute_url(self):
        return reverse("users:profile", kwargs={"username": self.user_slug})


class FriendRequest(models.Model):
    to_profile = models.ForeignKey(
        Profile,
        related_name="requests",
        on_delete=models.CASCADE,
        verbose_name="Заявки в друзья",
    )
    from_user = models.OneToOneField(
        get_user_model(), related_name="request_from", on_delete=models.CASCADE
    )
    to_user = models.OneToOneField(
        get_user_model(), related_name="request_to", on_delete=models.CASCADE
    )
    created = models.DateTimeField(auto_now_add=True)
