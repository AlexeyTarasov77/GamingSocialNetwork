import abc

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractBaseUser
from django.db.models import Q

User = get_user_model()


class AbstractUsersService(abc.ABC):
    @abc.abstractmethod
    def create_user(self, **data) -> AbstractBaseUser:
        pass

    @abc.abstractmethod
    def count_users(self) -> int:
        pass

    @abc.abstractmethod
    def get_suggested_users_per_user(self, user):
        pass


class UsersService(AbstractUsersService):
    @staticmethod
    def create_user(**data) -> AbstractBaseUser:
        user = User.objects.create_user(**data)
        return user

    @staticmethod
    def count_users() -> int:
        return User.objects.count()

    @staticmethod
    def get_suggested_users_per_user(user):
        print(user)
        profile = user.profile
        suggested_users = User.objects.filter(
            Q(id__in=profile.following.all()) | Q(id__in=profile.friends.all())
        )
        return suggested_users
