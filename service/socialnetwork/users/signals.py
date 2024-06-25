from django.dispatch import receiver
from allauth.account.signals import user_signed_up
from django.contrib.auth import get_user_model
from .models import Profile


@receiver(user_signed_up, sender=get_user_model())
def create_user_profile(request, user, **kwargs):
    """Creating profile after creating new user"""
    return Profile.objects.create(user=user)
