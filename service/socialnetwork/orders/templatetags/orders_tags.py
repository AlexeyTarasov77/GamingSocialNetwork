from django.template.library import Library
from orders.models import Order

register = Library()

@register.inclusion_tag("orders/components/order_table.html")
def show_order_table(orders: Order, many: bool = False):
    """
    Parameters:
    - order (Order): The order object to display.
    - many (bool): A flag indicating whether the order is a queryset or a single object.

    Returns:
    - dict: A dictionary containing the order and include_url values.
    """
    return {"orders": orders, "many": many}
