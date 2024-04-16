from django.shortcuts import get_object_or_404, render
from gameshop.models import ProductProxy
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST
from coupons.forms import CouponApplyForm

from .cart import Cart


# Create your views here.
def cart_view(request):
    coupon_form = CouponApplyForm()
    return render(request, "cart/cart.html", {"coupon_form": coupon_form})

@require_POST
def cart_add_or_update(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(ProductProxy, id=product_id) 
    quantity = int(request.POST.get("qty", 1))
    cart.add_or_update(product, quantity)
    # data = {"total_price": cart.get_total_price(), "total_items": len(cart)}
    return HttpResponse(len(cart))

@require_POST
def cart_remove(request, product_id): 
    cart = Cart(request)
    cart.delete(product_id)
    # data = {'total_price': cart.get_total_price(), 'total_items': len(cart)}
    return HttpResponse(cart.get_total_price())
