from django.contrib.auth import get_user_model
from django.test import Client, TestCase, RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware
from django.urls import reverse
from gameshop.models import ProductProxy
from .models import Order

User = get_user_model()


# Create your tests here.
class OrderCreateTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.client.login(username="testuser", password="12345")
        self.product = ProductProxy.objects.create(
            title="Example Product", price=10.0, brand="Example Brand"
        )
        self.factory = RequestFactory().post(
            reverse("cart:add", kwargs={"product_id": self.product.id}),
            {
                "product_qty": 2,
            },
        )
        self.middleware = SessionMiddleware(self.factory)
        self.middleware.process_request(self.factory)
        self.factory.session.save()

    def test_order_create(self):
        response = self.client.post(
            reverse("orders:order_create"),
            {
                "first_name": "TestName",
                "last_name": "TestSurname",
                "email": "b3yUH@example.com",
                "address": "Test Adress",
                "postal_code": "Test PostalCode",
                "city": "Test City",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Order.objects.filter(first_name="TestName", id=1).exists())

    def test_order_view(self):
        response = self.client.get(reverse("orders:order_create"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "orders/order_create.html")
