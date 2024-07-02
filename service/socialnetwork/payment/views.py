import logging
from decimal import Decimal

import stripe
from core.views import catch_exception
from django.conf import settings
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from orders.models import Order

# создать экземпляр Stripe
stripe.api_key = settings.STRIPE_SECRET_KEY
stripe.api_version = settings.STRIPE_API_VERSION


logger = logging.getLogger(__name__)


@catch_exception
def payment_process(request):
    """Create a stripe session and redirect it to the Stripe payment page."""
    order_id = request.session.get("order_id", None) or request.POST.get("order_id", None)
    order = get_object_or_404(Order, id=order_id)
    if request.method == "POST":
        logger.debug("Started processing payment for order %r", order)
        """
        line_items в session_data - массив обьектов с информацией о приобретаемых позициях в заказе:
            • price_data: информация, связанная с ценой;
            • unit_amount: сумма в центах, которую необходимо получить при оплате.
            • currency: используемая валюта в трехбуквенном формате ISO.
            • product_data: информация, связанная с товаром:
            • name: название товара;
            • quantity: число приобретаемых единиц товара.
        """
        session_data = {
            "mode": "payment",
            "client_reference_id": order.id,
            "success_url": request.build_absolute_uri(reverse_lazy("payment:completed")),
            "cancel_url": request.build_absolute_uri(reverse_lazy("payment:canceled")),
            "line_items": [
                {
                    "price_data": {
                        "unit_amount": int(item.price * Decimal("100")),
                        "currency": "usd",
                        "product_data": {
                            "name": item.product.title,
                        },
                    },
                    "quantity": item.quantity,
                }
                for item in order.items.all()
            ],
        }
        if order.coupon:
            stripe_coupon = stripe.Coupon.create(
                name=order.coupon.code,
                percent_off=order.discount,
                duration="once",
            )
            session_data["discounts"] = [{"coupon": stripe_coupon.id}]
            logger.debug("Applied coupon %s to order %r", stripe_coupon, order)

        session = stripe.checkout.Session.create(**session_data)
        logger.debug("Created stripe session %s", session)

        return redirect(session.url, code=303)
    else:
        return render(request, "payment/process.html", {"order": order})


@catch_exception
def payment_completed(request):
    """View successfull payment"""
    order_id = request.session.get("order_id", None)
    order = get_object_or_404(Order, id=order_id)
    if not order:
        logger.warning("No order found with id %s", order_id)
    return render(request, "payment/completed.html", {"order": order})


def payment_canceled(request):
    """View canceled payment"""
    return render(request, "payment/canceled.html")
