import logging

from cart.cart import Cart
from core.views import catch_exception
from django.http import HttpResponse
from django.views.decorators.http import require_POST

from .forms import CouponApplyForm
from .models import Coupon

logger = logging.getLogger(__name__)


@catch_exception
@require_POST
def coupon_apply(request):
    """View for applying coupon to the cart."""
    cart = Cart(request)
    form = CouponApplyForm(request.POST)
    if form.is_valid():
        code = form.cleaned_data["code"]
        code = form.cleaned_data["code"]
        try:
            coupon = Coupon.active_objects.get(code=code)
            request.session["coupon_id"] = coupon.id
            logger.info(
                "Coupon %r applied to cart by user with id %s", coupon, request.user.id
            )
        except Coupon.DoesNotExist:
            request.session["coupon_id"] = None
            logger.info(
                "User with id %s attempted to apply not existing coupon with code %s",
                request.user.id,
                code,
            )
            return HttpResponse("Такого купона не существует", status=406)
        return HttpResponse(cart.get_discounted_total_price())
