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
    """
    Model for ads (searching and recruiting).

    Attributes:
        title (CharField): Title of the ad.
        content (TextField): Content of the ad.
        favorites (ManyToManyField): Users who favorited the ad.
        game (CharField): Game of the ad.
        user (ForeignKey): User who created the ad.
        team (ForeignKey): Team associated with the ad.
        type (CharField): Type of the ad.
        time_create (DateTimeField): Time when the ad was created.
        time_update (DateTimeField): Time when the ad was last updated.
        photo (ImageField): Photo associated with the ad.
    """
    TYPE_CHOICES = {"SEARCHING": _("Поиск команды"), "RECRUITING": _("Набор в команду")}
    title = models.CharField(_("Заголовок"), max_length=200, db_index=True)
    content = models.TextField(_("Содержимое"), blank=True)
    favorites = models.ManyToManyField(
        User, related_name="favorite_ads", blank=True, verbose_name=_("Избранное")
    )
    game = models.CharField(_("Игра"), max_length=100, db_index=True)
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
        """Return string representation of the model."""
        return self.title

    def get_absolute_url(self):
        """Return absolute URL for the ad."""
        return reverse("teams:ad_detail", kwargs={"pk": self.pk})


class Team(SaveSlugMixin, models.Model):
    """
    Model for game teams.

    Attributes:
        name (CharField): Name of the team.
        logo (ImageField): Logo of the team.
        slug (SlugField): URL of the team.
        description (TextField): Description of the team.
        country (CountryField): Country of the team.
        rating (PositiveIntegerField): Rating of the team.
        game (CharField): Game of the team.
        time_create (DateTimeField): Time when the team was created.
        time_update (DateTimeField): Time when the team was last updated.
        founder (OneToOneField): User who founded the team.
        leader (OneToOneField): User who is the leader of the team.
    """
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
    game = models.CharField(_("Игра"), max_length=50, db_index=True)
    time_create = models.DateTimeField(_("Дата создания"), auto_now_add=True)
    time_update = models.DateTimeField(_("Дата обновления"), auto_now=True)
    founder = models.OneToOneField(
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

    @property
    def members(self):
        return self.members.all()

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
