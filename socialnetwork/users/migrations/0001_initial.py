# Generated by Django 5.0.1 on 2024-01-21 22:45

import django.db.models.deletion
import users.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_online', models.BooleanField(default=False)),
                ('image', models.ImageField(blank=True, null=True, upload_to=users.models.get_avatar_path)),
                ('bio', models.TextField(blank=True, null=True)),
                ('date_of_birth', models.DateTimeField(blank=True, null=True)),
                ('time_update', models.DateTimeField(auto_now=True)),
                ('following', models.ManyToManyField(blank=True, related_name='profile_following', to=settings.AUTH_USER_MODEL)),
                ('friends', models.ManyToManyField(blank=True, related_name='profile_friends', to=settings.AUTH_USER_MODEL)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
