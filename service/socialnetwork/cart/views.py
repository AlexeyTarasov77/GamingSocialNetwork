import logging

from core.views import catch_exception
from coupons.forms import CouponApplyForm
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_POST
from gameshop.models import ProductProxy
from gameshop.recommender import Recommender

from .cart import Cart

logger = logging.getLogger(__name__)


@catch_exception
def cart_view(request) -> HttpResponse:
    coupon_form = CouponApplyForm()
    rec = Recommender()
    cart = Cart(request)
    context = {"coupon_form": coupon_form}
    if len(cart) > 0:
        context["recommended_products"] = rec.suggest_products_for([item["product"] for item in cart])
    logger.info("Rendering cart with suggested products: %s", context.get("recommended_products"))
    return render(request, "cart/cart.html", context)


@catch_exception
@require_POST
def cart_add_or_update(request, product_id: int) -> HttpResponse:
    cart = Cart(request)
    product = get_object_or_404(ProductProxy, id=product_id)
    product = get_object_or_404(ProductProxy, id=product_id)
    quantity = int(request.POST.get("qty", 1))
    logger.info(f"Adding {quantity} of {product} to cart")
    cart.add_or_update(product, quantity)
    return HttpResponse(len(cart))


@catch_exception
@require_POST
def cart_remove(request, product_id) -> HttpResponse:
    cart = Cart(request)
    cart.delete(product_id)
    logger.info(f"Removing {product_id} from cart")
    return HttpResponse(cart.get_total_price())
