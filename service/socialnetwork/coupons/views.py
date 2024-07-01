from cart.cart import Cart
from django.http import HttpResponse
from django.views.decorators.http import require_POST

from .forms import CouponApplyForm
from .models import Coupon

# Create your views here.


@require_POST
def coupon_apply(request):
    """View for applying coupon to the cart."""
    cart = Cart(request)
    form = CouponApplyForm(request.POST)
    if form.is_valid():
        code = form.cleaned_data["code"]
        try:
            coupon = Coupon.active_objects.get(code=code)
            request.session["coupon_id"] = coupon.id
        except Coupon.DoesNotExist:
            request.session["coupon_id"] = None
            # form.add_error('code', 'Такого купона не существует')
            return HttpResponse("Такого купона не существует", status=406)
        return HttpResponse(cart.get_discounted_total_price())
