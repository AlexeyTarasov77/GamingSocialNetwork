from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext as _
from django_countries.fields import CountryField
from gameblog.mixins import SaveSlugMixin

User = get_user_model()


# Create your models here.
class Ad(models.Model):
    TYPE_CHOICES = {"SEARCHING": "Поиск команды", "RECRUITING": "Набор в команду"}
    title = models.CharField(_("Заголовок"), max_length=200, db_index=True)
    content = models.TextField(_("Содержимое"), blank=True)
    favorites = models.ManyToManyField(
        User, related_name="favorite_ads", blank=True, verbose_name=_("Избранное")
    )
    game = models.ForeignKey(
        "Game",
        on_delete=models.CASCADE,
        verbose_name=_("Игра"),
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=_("Автор"),
        related_name="search_ads",
    )
    team = models.ForeignKey(
        "Team", verbose_name=_("Команда"), on_delete=models.CASCADE, null=True
    )
    type = models.CharField(
        _("Тип обьявления"),
        choices=TYPE_CHOICES,
        db_index=True,
        default=TYPE_CHOICES["SEARCHING"],
    )
    time_create = models.DateTimeField(_("Дата создания"), auto_now_add=True)
    time_update = models.DateTimeField(_("Дата обновления"), auto_now=True)
    photo = models.ImageField(
        _("Фото"), upload_to="photos/searchteam/", blank=True, null=True
    )

    class Meta:
        ordering = ["-time_create"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("teams:ad_detail", kwargs={"pk": self.pk})


class Team(SaveSlugMixin, models.Model):
    name = models.CharField(_("Имя"), max_length=200, db_index=True)
    logo = models.ImageField(
        _("Логотип"), upload_to="photos/gameteams/", blank=True, null=True
    )
    slug = models.SlugField(
        _("URL"), max_length=200, db_index=True, unique=True, blank=True
    )
    description = models.TextField(_("Про команду"), blank=True, null=True)
    country = CountryField(_("Страна"), blank=True, null=True)
    rating = models.PositiveIntegerField(
        _("Рейтинг"), default=0, blank=True, validators=[MaxValueValidator(10)]
    )  # что то вроде репутации команды
    game = models.ForeignKey(
        "Game",
        on_delete=models.CASCADE,
        verbose_name=_("Игра"),
    )
    time_create = models.DateTimeField(_("Дата создания"), auto_now_add=True)
    time_update = models.DateTimeField(_("Дата обновления"), auto_now=True)
    founder = models.ForeignKey(
        User,
        verbose_name=_("Основатель"),
        on_delete=models.SET_NULL,
        related_name="team_founder",
        null=True,
    )
    leader = models.OneToOneField(
        User,
        verbose_name=_("Руководитель"),
        on_delete=models.CASCADE,
        related_name="team_leader",
        null=True,
    )

    class Meta:
        ordering = ["-rating"]

    def __str__(self):
        return self.name

    def get_logo(self):
        if not self.logo:
            return settings.DEFAULT_IMAGE_URL
        return self.logo.url

    def get_absolute_url(self):
        return reverse("teams:team_detail", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        super().save(*args, slug_field="slug", slugify_value=self.name, **kwargs)


class TeamJoinRequest(models.Model):
    to_team = models.ForeignKey(
        "Team", verbose_name=_("Команда"), on_delete=models.CASCADE
    )
    from_user = models.ForeignKey(
        User, verbose_name=_("Пользователь"), on_delete=models.CASCADE
    )
    time_create = models.DateTimeField(_("Дата создания"), auto_now_add=True)
    time_update = models.DateTimeField(_("Дата обновления"), auto_now=True)

    def __str__(self):
        return f"{self.from_user} wants to join {self.to_team}"


class Game(SaveSlugMixin, models.Model):
    name = models.CharField(_("Игра"), max_length=200, db_index=True)
    slug = models.SlugField(
        _("URL"), max_length=200, db_index=True, unique=True, blank=True
    )
    logo = models.ImageField(_("Логотип"), upload_to="photos/gameteams/games/")

    @property
    def popularity(self):
        return self.bounded_teams.count()
    
    def save(self, *args, **kwargs):
        super().save(*args, slug_field="slug", slugify_value=self.name, **kwargs)

    def __str__(self):
        return self.name
