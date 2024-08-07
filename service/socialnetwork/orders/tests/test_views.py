from django.contrib.sessions.middleware import SessionMiddleware
from django.test import Client, RequestFactory, TestCase
from django.urls import reverse
from django.utils.translation import activate
from gameshop.tests.factories import ProductProxyFactory
from users.tests.factories import UserFactory

from orders.models import Order


class OrderCreateTestCase(TestCase):
    def setUp(self):
        activate("en")
        self.client = Client()
        self.user = UserFactory.create()
        self.client.login(username=self.user.username, password="password123")
        self.product = ProductProxyFactory.create()
        self.factory = RequestFactory().post(
            reverse("cart:add", kwargs={"product_id": self.product.id}),
            {"product_qty": 2},
        )
        self.middleware = SessionMiddleware(self.factory)
        self.middleware.process_request(self.factory)
        self.factory.session.save()

    def test_order_create(self):
        data = {
            "first_name": "TestName",
            "last_name": "TestSurname",
            "email": "b3yUH@example.com",
            "address": "Test Adress",
            "postal_code": "Test PostalCode",
            "city": "Test City",
        }
        response = self.client.post(
            reverse("orders:order_create"),
            data,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Order.objects.filter(**data).exists())

    def test_order_view(self):
        response = self.client.get(reverse("orders:order_create"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "orders/order_create.html")
