import factory
import factory.fuzzy as fuzzy
from django.utils import timezone
from factory.django import DjangoModelFactory


class CouponFactory(DjangoModelFactory):
    code = factory.Sequence(lambda n: "code{0}".format(n))
    discount = fuzzy.FuzzyInteger(1, 100)
    valid_from = fuzzy.FuzzyDateTime(timezone.now(), timezone.now() + timezone.timedelta(days=30))
    valid_to = fuzzy.FuzzyDateTime(
        timezone.now() + timezone.timedelta(days=30), timezone.now() + timezone.timedelta(days=60)
    )

    class Meta:
        model = "coupons.Coupon"
