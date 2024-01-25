from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model

# Create your models here.

EVENT_TYPE_CHOICES = {
    'tournament': 'Турнир',
    'beta_test': 'Бета-тест',
    'game_release': 'Релиз игры',
    'update': 'Обновление',
    'in-game_event': 'Игровое событие',
    'esports_match': 'Матч',
}

class Event(models.Model):
    title = models.CharField(max_length=255, db_index = True)
    description = models.TextField(blank = True)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name = 'event_author')
    start_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    event_type = models.BooleanField(choices = EVENT_TYPE_CHOICES, db_index = True)
    


    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("Event_detail", kwargs={"pk": self.pk})
