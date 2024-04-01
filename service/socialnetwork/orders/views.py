from django.shortcuts import redirect, render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from . import forms
from .models import Order, OrderItem
from .tasks import confirm_order
from cart.cart import Cart
from django.db import transaction

# Create your views here.

@login_required
def order_create_view(request):
    if request.method == "POST":
        cart = Cart(request)
        form = forms.OrderCreateForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                order = form.save(commit=False)
                cd = form.cleaned_data
                order.user = request.user
                order.save()
                order_items = [OrderItem(order=order, product=item["product"], price=item["price"], quantity=item["qty"]) for item in cart]
                OrderItem.objects.bulk_create(order_items)
                cart.clear()
                confirm_order.delay(order.id, f"{cd["first_name"]} {cd['last_name']}", cd["email"])
                return HttpResponseRedirect(reverse("orders:order_created"))
    else:
        form = forms.OrderCreateForm()
    return render(request, "orders/order_create.html", {"form": form})
