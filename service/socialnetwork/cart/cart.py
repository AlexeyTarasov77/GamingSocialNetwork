from decimal import Decimal
from coupons.models import Coupon

from django.http import HttpRequest
from gameshop.models import ProductProxy, Product
from django.conf import settings


class Cart:
    """Cart class for managing the cart"""
    def __init__(self, request: HttpRequest) -> None:
        self.session = request.session

        cart = self.session.get(settings.CART_SESSION_KEY)

        if not cart:
            cart = self.session[settings.CART_SESSION_KEY] = {}

        self.cart = cart

        self.coupon_id = self.session.get("coupon_id")

    @property
    def coupon(self) -> Coupon | None:
        """Method for getting applied coupon if any"""
        if self.coupon_id:
            try:
                return Coupon.active_objects.get(id=self.coupon_id)
            except Coupon.DoesNotExist:
                pass
            return None

    def __len__(self):
        """Method for getting the total quantity of items in the cart"""
        return sum([item["qty"] for item in self.cart.values()])

    def __iter__(self):
        """Iterate over the cart. Adds total computed fields to each item"""
        product_ids = self.cart.keys()  # ['1', '2', '3', ...]
        products = ProductProxy.objects.filter(id__in=product_ids)
        cart = self.cart.copy()

        for product in products:
            cart[str(product.id)]["product"] = product

        for (
            item
        ) in (
            cart.values()
        ):  # {'product': product, 'qty': 2, 'price': 1000, 'total': 2000}
            item["price"] = Decimal(item["price"])
            item["total"] = item["price"] * item["qty"]
            yield item

    def __contains__(self, product_id):
        """Check whether a product is in the cart."""
        return str(product_id) in self.cart

    def save(self) -> None:
        """Save the cart."""
        self.session.modified = True

    def add_or_update(self, product: Product, quantity: int = 1):
        """Add a product to the cart or update its quantity if it already exists."""

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
        """Delete a product from the cart if it is there."""
        product_id = str(product_id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def clear(self) -> None:
        """Remove all items in the cart."""
        self.session[settings.CART_SESSION_KEY] = {}
        self.save()

    def get_discount(self) -> Decimal:
        """Returns the discount of applied coupon if any."""
        if self.coupon:
            return (self.coupon.discount / Decimal(100)) * self.get_total_price()
        return Decimal(0)

    def get_discounted_total_price(self) -> Decimal:
        """Get total cart price with computed discount."""
        return self.get_total_price() - self.get_discount()

    def get_total_price(self) -> Decimal:
        return sum(Decimal(item["price"]) * item["qty"] for item in self.cart.values())
