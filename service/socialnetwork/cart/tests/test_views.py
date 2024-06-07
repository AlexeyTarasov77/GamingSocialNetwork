from django.test import TestCase, Client, RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware
from django.urls import reverse
from django.utils.translation import activate
from gameshop.models import ProductProxy
from cart.views import cart_add_or_update, cart_remove
from gameshop.tests.factories import ProductProxyFactory
# Create your tests here.
class CartViewTestCase(TestCase):

    def setUp(self):
        activate('en')
        self.client = Client()
        self.product = ProductProxyFactory.create()
        self.factory = RequestFactory()
        self.middleware = SessionMiddleware(self.factory)
        self.middleware.process_request(self.factory)
        self.factory.session.save()
        
    def test_cart_view(self):
        response = self.client.get(reverse("cart:view"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "cart/cart.html")
        
    def test_cart_add(self):
        test_quantity = 2
        request = self.factory.post(
            reverse('cart:add', args=[self.product.id]),
            {'product_qty': test_quantity}
        )
        response = cart_add_or_update(request, self.product.id)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(request.session['cart'])
        self.assertEqual(len(request.session['cart']), 2)
        self.assertIn(self.product.id, request.session['cart'])
        
class CartAddTestCase(TestCase):
    
    def setUp(self):
        self.client = Client()
        self.product = ProductProxy.objects.create(title='Example Product', price=10.0, brand='Example Brand')
        self.factory = RequestFactory().post(reverse('cart:add', args=[self.product.id]), {'product_qty': 2})
        self.middleware = SessionMiddleware(self.factory)
        self.middleware.process_request(self.factory)
        self.factory.session.save()
        
    def test_cart_add(self):
        request = self.factory
        response = cart_add_or_update(request, self.product.id)
        self.assertEqual(response.status_code, 200)
        
        
class CartRemoveTestCase(TestCase):
    
    def setUp(self):
        self.client = Client()
        self.product = ProductProxy.objects.create(title='Example Product', price=10.0, brand='Example Brand')
        self.factory = RequestFactory().post(reverse('cart:remove', args=[self.product.id]))
        self.middleware = SessionMiddleware(self.factory)
        self.middleware.process_request(self.factory)
        self.factory.session.save()
        
    def test_cart_remove(self):
        request = self.factory
        response = cart_remove(request, self.product.id)
        self.assertEqual(response.status_code, 200)
        