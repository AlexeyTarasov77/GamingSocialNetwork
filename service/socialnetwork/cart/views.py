from django.shortcuts import get_object_or_404, render
from gameshop.models import ProductProxy
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from .cart import Cart


# Create your views here.
def cart_view(request):
    return render(request, "cart/cart.html")

@require_POST
def cart_add_or_update(request):
    cart = Cart(request)
    product = get_object_or_404(ProductProxy, id=request.POST.get("product_id")) 
    quantity = int(request.POST.get("quantity"))
    cart.add_or_update(product, quantity)
    data = {"total_price": cart.get_total_price(), "total_items": len(cart)}
    return JsonResponse(data)

@require_POST
def cart_remove(request): 
    cart = Cart(request)
    product_id = request.POST.get('product_id')
    cart.delete(product_id)
    data = {'total_price': cart.get_total_price(), 'total_items': len(cart)}
    return JsonResponse(data)
