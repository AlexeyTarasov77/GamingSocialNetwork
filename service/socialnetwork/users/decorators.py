
from .models import Profile
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404


def owner_required(view_func):
    def wrapper_func(request, *args, **kwargs):
        profile = get_object_or_404(Profile, user_slug=kwargs["username"])
        if request.user == profile.user:
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponseForbidden()
    return wrapper_func
    
    