import factory
import factory.fuzzy
from django.contrib.auth import get_user_model
from factory.django import DjangoModelFactory
from users.models import Profile

User = get_user_model()


class UserFactory(DjangoModelFactory):
    username = factory.Sequence(lambda n: "user{0}".format(n))
    password = factory.django.Password("password123")

    class Meta:
        model = User


class ProfileFactory(factory.django.DjangoModelFactory):
    user = factory.SubFactory(UserFactory)

    class Meta:
        model = Profile
