from decimal import Decimal

from django.http import HttpRequest
from gameshop.models import ProductProxy, Product
from django.conf import settings


class Cart:

    def __init__(self, request: HttpRequest) -> None:
        assert isinstance(request, HttpRequest), "request must be an HttpRequest object"
        self.session = request.session

        cart = self.session.get(settings.CART_SESSION_KEY)

        if not cart:
            cart = self.session[settings.CART_SESSION_KEY] = {}

        self.cart = cart

    def __len__(self):  # вернуть сумму количества товаров
        return sum([item["qty"] for item in self.cart.values()])

    def __iter__(self):
        product_ids = self.cart.keys()  # ['1', '2', '3', ...]
        products = ProductProxy.objects.filter(id__in=product_ids)
        cart = self.cart.copy()

        for product in products:
            cart[str(product.id)]["product"] = product

        for (
            item
        ) in (
            cart.values()
        ):  # {'product': product, 'qty': 1, 'price': 1000, 'total': 1000}
            item["price"] = Decimal(item["price"])
            item["total"] = item["price"] * item["qty"]
            yield item

    def save(self):
        """Save the cart"""
        self.session.modified = True

    def add_or_update(self, product: Product, quantity: int = 1):
        """Add a product to the cart or update its quantity"""

        product_id = str(product.id)

        if product_id not in self.cart:
            self.cart[product_id] = {
                "qty": quantity,
                "price": str(product.final_price),
            }
        else:
            self.cart[product_id]["qty"] = quantity

        self.save()

    def delete(self, product_id: str | int):
        product_id = str(product_id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def get_total_price(self):
        return sum(Decimal(item["price"]) * item["qty"] for item in self.cart.values())
