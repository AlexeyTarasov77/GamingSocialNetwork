import logging

import stripe
from core.views import catch_exception
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from gameshop.recommender import Recommender
from orders.models import Order

from .tasks import payment_completed

logger = logging.getLogger(__name__)


@catch_exception
@csrf_exempt
def stripe_webhook(request):
    """Webhook that is triggered after stripe payment.
    If payment was successful, the order is marked as paid.
    """
    payload = request.body
    logger.debug("Got payload: %s", payload)
    sig_header = request.META["HTTP_STRIPE_SIGNATURE"]
    webhook_secret = settings.STRIPE_WEBHOOK_SECRET
    event = None
    try:
        event = stripe.Webhook.construct_event(payload, sig_header, webhook_secret)
    except ValueError:
        # Invalid payload
        logger.error("Invalid payload: %s", payload)
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        # Invalid signature
        logger.error("Invalid signature: %s", sig_header)
        return HttpResponse(status=400)

    if event.type == "checkout.session.completed":
        session = event.data.object
        logger.debug("Checkout session completed: %s", session)
        if session.mode == "payment" and session.payment_status == "paid":
            logger.debug("Payment completed")
            order_id = session.client_reference_id
            order = get_object_or_404(Order, id=order_id)
            order.paid = True
            order.stripe_id = session.payment_intent
            rec = Recommender()
            rec.products_bought(order.items.all())
            logger.debug("Registered bought products in recommender")
            order.save()
            logger.debug("Added stripe_id %s to order and mark it as paid.", order.stripe_id)
            payment_completed.delay(order.id)

    return HttpResponse()
