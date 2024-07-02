from django.contrib.auth.models import AbstractBaseUser
from gameblog.models import Ad
from posts.services.m2m_toggle import ToggleM2MBaseService


class AdService:
    @staticmethod
    def bookmark_ad(ad: Ad, user: AbstractBaseUser) -> bool:
        return ToggleM2MBaseService(ad, "favorites", user).execute()
