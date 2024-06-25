import factory.fuzzy
from users.models import Profile
import factory
from django.contrib.auth import get_user_model
from factory.django import DjangoModelFactory

User = get_user_model()

class UserFactory(DjangoModelFactory):
    username = factory.Sequence(lambda n: 'user{0}'.format(n))
    password = factory.PostGenerationMethodCall('set_password', 'password123') 

    @factory.post_generation
    def set_password(obj, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            obj.set_password(extracted)
        else:
            obj.set_password('password123')

    class Meta:
        model = User

            
class ProfileFactory(factory.django.DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    class Meta:
        model = Profile