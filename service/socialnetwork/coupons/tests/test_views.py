from django.test import TestCase, Client
from .factories import CouponFactory
from django.urls import reverse
from django.utils.translation import activate

# Create your tests here.
class CouponTestCase(TestCase):
    def setUp(self) -> None:
        activate('en')
        self.client = Client()
        self.coupon = CouponFactory.create()
        
    def test_coupon_apply(self):
        response = self.client.post(reverse('coupons:apply'), {'code': self.coupon.code})
        self.assertEqual(response.status_code, 200)