import os
from enum import Enum

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractBaseUser
from django.db import models, transaction
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
    user_slug = models.SlugField(verbose_name="URL профиля", unique=True, null=True, blank=True)
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
    bio = models.TextField(blank=True, default="", verbose_name=_("Биография"))
    date_of_birth = models.DateTimeField(null=True, blank=True, verbose_name=_("Дата рождения"))
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

    def save(self, *args, **kwargs):
        return super().save(*args, slug_field="user_slug", slugify_value=self.user.username, **kwargs)

    def get_absolute_url(self):
        return reverse("users:profile", kwargs={"username": self.user_slug})

    @property
    def is_team_leader(self):
        if self.team:
            return self.team.leader == self.user
        return False

    @property
    def age(self):
        if self.date_of_birth:
            return (timezone.now() - self.date_of_birth).days // 365

    class Actions(str, Enum):
        ADD = "add"
        REMOVE = "remove"

    def _update_follow_rel(
        self, target_user: AbstractBaseUser, action: Actions
    ) -> None:
        assert action in self.Actions, f"Invalid action: {action}"
        with transaction.atomic():
            getattr(self.following, action)(target_user)
            getattr(target_user.profile.followers, action)(self.user)

    def _update_friendship_rel(
        self, target_user: AbstractBaseUser, action: Actions
    ) -> None:
        assert action in self.Actions, f"Invalid action: {action}"
        with transaction.atomic():
            getattr(self.friends, action)(target_user)
            getattr(target_user.profile.friends, action)(self.user)

    def follow_user(self, target_user: AbstractBaseUser) -> None:
        self._update_follow_rel(target_user, self.Actions.ADD)

    def unfollow_user(self, target_user: AbstractBaseUser) -> None:
        self._update_follow_rel(target_user, self.Actions.REMOVE)

    def add_friend(self, target_user: AbstractBaseUser) -> None:
        self._update_friendship_rel(target_user, self.Actions.ADD)

    def remove_friend(self, target_user: AbstractBaseUser) -> None:
        self._update_friendship_rel(target_user, self.Actions.REMOVE)

    def get_image(self):
        return self.image.url if self.image else "/static/users/images/profile.jpeg"

    def get_background_image(self):
        return self.bg_image.url if self.bg_image else "/static/users/images/background.jpeg"


class ProfileTeamsHistory(models.Model):
    profile = models.ForeignKey("Profile", verbose_name=_("Пользователь"), on_delete=models.CASCADE)
    team = models.ForeignKey("gameteams.Team", verbose_name=_("Команда"), on_delete=models.CASCADE)
    date_joined = models.DateTimeField(_("Дата присоединения"), auto_now_add=True)
    date_left = models.DateTimeField(_("Дата выхода"), null=True, blank=True)

    def __str__(self):
        return f"{self.profile.user} joined {self.team}"


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
    to_user = models.OneToOneField(get_user_model(), related_name="request_to", on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Заявка в друзья от {self.from_user}"
