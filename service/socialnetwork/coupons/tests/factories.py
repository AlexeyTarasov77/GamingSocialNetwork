from factory.django import DjangoModelFactory
import factory, factory.fuzzy as fuzzy
from users.tests.factories import UserFactory
from django.utils import timezone

class CouponFactory(DjangoModelFactory):

    code = factory.Sequence(lambda n: 'code{0}'.format(n))
    discount = fuzzy.FuzzyInteger(1, 100)
    valid_from = fuzzy.FuzzyDateTime(timezone.now())
    valid_to = fuzzy.FuzzyDateTime(timezone.now(), timezone.now() + timezone.timedelta(days=30))
    class Meta:
        model = 'coupons.Coupon'