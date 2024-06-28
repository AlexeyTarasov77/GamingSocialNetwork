import weasyprint
from cart.cart import Cart
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from users.decorators import owner_required

from . import forms
from .models import Order, OrderItem
from .tasks import confirm_order

# Create your views here.


def order_create_view(request):
    """View for creating an order"""
    if not request.user.is_authenticated:
        return HttpResponse(status=401)
    if request.method == "POST":
        cart = Cart(request)
        form = forms.OrderCreateForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                order = form.save(commit=False)
                cd = form.cleaned_data
                order.user = request.user
                if cart.coupon:
                    order.coupon = cart.coupon
                    order.discount = cart.coupon.discount
                order.save()
                order_items = [
                    OrderItem(
                        order=order, product=item["product"],
                        price=item["price"], quantity=item["qty"]
                    )
                    for item in cart
                ]
                OrderItem.objects.bulk_create(order_items)
                cart.clear()
                confirm_order.delay(order.id, f"{cd["first_name"]} {cd['last_name']}", cd["email"])
                # save created order id in the session to use it later in payment
                request.session["order_id"] = order.id
                return HttpResponse(request.build_absolute_uri(reverse_lazy("payment:process")))
    else:
        form = forms.OrderCreateForm()
    return render(request, "orders/order_create.html", {"form": form})


@owner_required("orders")
def order_detail_view(request, order_id):
    """View details of an order"""
    order = get_object_or_404(Order, id=order_id)
    return render(request, "orders/order_detail.html", {"order": order})


@owner_required("orders")
def order_to_pdf(request, order_id):
    """View PDF of an order"""
    order = get_object_or_404(Order, id=order_id)
    html = render_to_string('orders/pdf_invoice.html', {'order': order})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename=order_{order.id}.pdf'
    weasyprint.HTML(string=html).write_pdf(
        response,
        stylesheets=[
            weasyprint.CSS('https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css')
        ]
    )
    return response
