from django.contrib import admin

from .models import Ad, Game, Team, TeamJoinRequest

# Register your models here.
admin.site.register([Team, TeamJoinRequest, Ad, Game])
