
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractBaseUser
from django.db.models import Q, QuerySet

User = get_user_model()


class UsersService:

    @staticmethod
    def count_users() -> int:
        return User.objects.count()

    @staticmethod
    def get_suggested_users_per_user(user: AbstractBaseUser) -> QuerySet[AbstractBaseUser]:
        print(user)
        profile = user.profile
        suggested_users = User.objects.filter(
            Q(id__in=profile.following.all()) | Q(id__in=profile.friends.all())
        )
        return suggested_users
