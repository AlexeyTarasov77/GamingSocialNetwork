from io import BytesIO

import weasyprint
from celery import shared_task
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from orders.models import Order


@shared_task
def payment_completed(order_id):
    """Sends email confirmation after successful payment with pdf invoice."""
    order = Order.objects.get(id=order_id)
    # create invoice e-mail
    subject = f"™GameShop - GamingSocialNetwork. Фактура №. {order.id}"
    message = f"""Доброго времени суток, {order.full_name}!\n\n
                Оплата прошла успешно! Ниже вы можете посмотреть PDF фактуру вашего заказа.\n
                Спасибо за покупку!"""
    email = EmailMessage(subject, message, None, [order.email])
    html = render_to_string("orders/pdf_invoice.html", {"order": order})
    stylesheets = [
        weasyprint.CSS(
            "https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css"
        )
    ]
    io = BytesIO()
    weasyprint.HTML(string=html).write_pdf(io, stylesheets=stylesheets)
    email.attach(f"order{order.id}_invoice.pdf", io.getvalue(), "application/pdf")
    email.send()
