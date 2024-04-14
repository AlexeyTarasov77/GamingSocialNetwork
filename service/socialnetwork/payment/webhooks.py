from django.conf import settings
from django.shortcuts import get_object_or_404
import stripe
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .tasks import payment_completed
from orders.models import Order


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META["HTTP_STRIPE_SIGNATURE"]
    webhook_secret = settings.STRIPE_WEBHOOK_SECRET
    event = None
    try:
        event = stripe.Webhook.construct_event(payload, sig_header, webhook_secret)
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    if event.type == "checkout.session.completed":
        session = event.data.object
        if session.mode == "payment" and session.payment_status == "paid":
            order_id = session.client_reference_id
            order = get_object_or_404(Order, id=order_id)
            order.paid = True
            order.stripe_id = session.payment_intent
            order.save()
            payment_completed.delay(order.id)

    return HttpResponse()
