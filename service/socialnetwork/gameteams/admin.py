from django.contrib import admin
from .models import Team, Ad, TeamJoinRequest

# Register your models here.
admin.site.register([Team, TeamJoinRequest, Ad])