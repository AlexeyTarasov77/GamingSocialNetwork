from django.shortcuts import get_object_or_404, render
from gameshop.models import ProductProxy
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from coupons.forms import CouponApplyForm
from gameshop.recommender import Recommender

from .cart import Cart


# Create your views here.
def cart_view(request):
    coupon_form = CouponApplyForm()
    rec = Recommender()
    cart = Cart(request)
    context = {"coupon_form": coupon_form}
    if len(cart) > 0:
        context["recommended_products"] = rec.suggest_products_for(
            [item["product"] for item in cart]
        )
    return render(request, "cart/cart.html", context)


@require_POST
def cart_add_or_update(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(ProductProxy, id=product_id)
    quantity = int(request.POST.get("qty", 1))
    print(quantity, request.POST.get("qty"))
    cart.add_or_update(product, quantity)
    # data = {"total_price": cart.get_total_price(), "total_items": len(cart)}
    return HttpResponse(len(cart))


@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    cart.delete(product_id)
    # data = {'total_price': cart.get_total_price(), 'total_items': len(cart)}
    return HttpResponse(cart.get_total_price())
