from celery import shared_task
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from .models import Order

@shared_task
def confirm_order(order_id: int, full_name: str, email: str):
    order = get_object_or_404(Order.objects.prefetch_related("items"), id=order_id)
    subject = f"Здравствуйте, {full_name}! Ваш заказ No{order.id} успешно оформлен."
    order_items = """\n""".join([f"Товар: {item.product.title}, Цена: {item.price}, Количество: {item.quantity}" for item in order.items.all()])
    message = (
        f"""
        Заказ No{order.id} на сумму {order.get_total_cost()} поступил в обработку и ожидает оплаты.\n 
        Детали заказа:\n
        Имя: {order.first_name}, Фамилия: {order.last_name}, Email: {order.email}, Адрес: {order.address}, Почтовый индекс: {order.postal_code}, Город: {order.city}.
        Товары в заказе:\n
        {order_items}
        """
    )
    send_mail(subject, message, None, [email])