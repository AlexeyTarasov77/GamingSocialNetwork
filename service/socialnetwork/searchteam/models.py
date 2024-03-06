from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

# Create your models here.
class Team(models.Model):
    STATUS_CHOICES = {
        'SEARCHING': 'Поиск команды',
        'RECRUITING': 'Набор в команду'
    }
    title = models.CharField(max_length = 200, db_index = True)
    description = models.TextField(blank = True)
    game_type = models.CharField(max_length = 100, db_index = True)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name = 'team_author')
    status = models.BooleanField(choices = STATUS_CHOICES, db_index = True)
    time_create = models.DateTimeField(auto_now_add=True)
    needed_players = models.IntegerField(blank=True)
    team_logo = models.ImageField(upload_to='photos/searchteam/', blank=True)
    
    

    class Meta:
        ordering = ['-time_create']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("_detail", kwargs={"pk": self.pk})
