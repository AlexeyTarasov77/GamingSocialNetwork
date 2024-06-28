import factory
from factory import fuzzy
from django.contrib.auth import get_user_model
from gameteams.models import Team, Game
from users.tests.factories import UserFactory
from faker import Faker
from pytils.translit import slugify

faker = Faker()

User = get_user_model()

class GameFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Game
    name = fuzzy.FuzzyText()
    logo = factory.LazyAttribute(lambda _: faker.image_url())

class TeamFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Team
    name = fuzzy.FuzzyText()
    slug = factory.LazyAttribute(lambda obj: slugify(obj.name))
    description = fuzzy.FuzzyText()
    rating = fuzzy.FuzzyInteger(0, 10)
    game = factory.SubFactory(GameFactory)
    leader = factory.SubFactory(UserFactory)
    founder = factory.SubFactory(UserFactory)
    
    
    