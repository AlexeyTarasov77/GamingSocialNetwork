import factory.fuzzy
from factory.django import DjangoModelFactory
from users.tests.factories import UserFactory

class PostFactory(DjangoModelFactory):
    class Meta:
        model = "posts.Post"

    title = factory.fuzzy.FuzzyText()
    content = factory.fuzzy.FuzzyText()
    author = factory.SubFactory(UserFactory)
    