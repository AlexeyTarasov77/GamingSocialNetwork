# Generated by Django 5.0.1 on 2024-01-25 20:18

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(db_index=True, max_length=255)),
                ('description', models.TextField(blank=True)),
                ('start_date', models.DateTimeField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('event_type', models.BooleanField(choices=[('tournament', 'Турнир'), ('beta_test', 'Бета-тест'), ('game_release', 'Релиз игры'), ('update', 'Обновление'), ('in-game_event', 'Игровое событие'), ('esports_match', 'Матч')], db_index=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='event_author', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
