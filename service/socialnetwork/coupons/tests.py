from django.test import TestCase, Client
from .models import Coupon
from django.urls import reverse

# Create your tests here.
class CouponTestCase(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.coupon = Coupon.objects.create(code='fds232des234124gf34s4', valid_from='2023-01-01', valid_to='2025-01-01', discount=10, active=True)
        
    def test_coupon_apply(self):
        response = self.client.post(reverse('coupons:apply'), {'code': self.coupon.code})
        self.assertEqual(response.status_code, 200)