from django.test import TestCase, Client, RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware
from django.urls import reverse
from django.utils.translation import activate
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
        
    def init_session(self, request) -> None:
        self.middleware.process_request(request)
        request.session.save()
        
    def test_cart_view(self):
        response = self.client.get(reverse("cart:view"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "cart/cart.html")
        
    def test_cart_add(self):
        test_quantity = 2
        request = self.factory.post(
            reverse('cart:add', args=[self.product.id]),
            {'qty': test_quantity}
        )
        self.init_session(request)
        response = cart_add_or_update(request, self.product.id)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(request.session['cart'])
        self.assertEqual(int(response.content.decode()), 2) # response should return valid quantity
        self.assertEqual(request.session['cart'][str(self.product.id)]['qty'], 2) # cart should contain valid quantity
        
    def test_cart_remove(self):
        request = self.factory.post(reverse('cart:remove', args=[self.product.id]))
        self.init_session(request)
        response = cart_remove(request, self.product.id)
        self.assertEqual(response.status_code, 200)
        