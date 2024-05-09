from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.translation import gettext as _
from gameblog.mixins import SaveSlugMixin

User = get_user_model()


# Create your models here.
class Ad(models.Model):
    TYPE_CHOICES = {
        'SEARCHING': 'Поиск команды',
        'RECRUITING': 'Набор в команду'
    }
    title = models.CharField(_("Заголовок"), max_length = 200, db_index = True)
    description = models.TextField(_("Описание"), blank = True)
    game = models.CharField(_("Игра"), max_length = 100, db_index = True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_("Автор"), related_name = 'search_ads')
    team = models.ForeignKey("Team", verbose_name=_("Команда"), on_delete=models.CASCADE)
    type = models.BooleanField(_("Тип обьявления"), choices = TYPE_CHOICES, db_index = True, default=TYPE_CHOICES["SEARCHING"])
    time_create = models.DateTimeField(_("Дата создания"), auto_now_add=True)
    time_update = models.DateTimeField(_("Дата обновления"), auto_now=True)
    photo = models.ImageField(_("Фото"), upload_to='photos/searchteam/', blank=True, null=True)
    
    

    class Meta:
        ordering = ['-time_create']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("_detail", kwargs={"pk": self.pk})


class Team(SaveSlugMixin, models.Model):
    name = models.CharField(_("Имя"), max_length = 200, db_index = True)
    logo = models.ImageField(_("Логотип"), upload_to='photos/gameteams/', blank=True, null=True)
    slug = models.SlugField(_("URL"), max_length = 200, db_index = True, unique=True)
    description = models.TextField(_("Про команду"), blank = True, null=True)
    game = models.CharField(_("Игра"), max_length = 50, db_index = True)
    founder = models.OneToOneField(User, verbose_name=_("Основатель"), on_delete=models.SET_NULL, related_name = 'team_founder', null=True)
    leader = models.OneToOneField(User, verbose_name=_("Руководитель"), on_delete=models.CASCADE, related_name = 'team_leader', null=True)
    
    @property
    def members(self):
        return self.members.all()
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("model_detail", kwargs={"slug": self.slug})
    
    def save(self, *args, **kwargs):
        super().save(*args, slug_field="slug", slugify_field="name", **kwargs)
    