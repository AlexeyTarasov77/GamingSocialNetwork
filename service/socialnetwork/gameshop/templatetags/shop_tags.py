from django import template
from django.utils.safestring import mark_safe
from cart.cart import Cart

register = template.Library()

@register.filter(name="fp")
def format_price(value):
    value = str(value)
    if value == "0.00":
        return mark_safe("<span class='text-success'>Бесплатно</span>")
    else:
        return f"$ {value}"

@register.simple_tag
def cart_len(cart: Cart):
    cart_len = len(cart)
    if cart_len > 99:
        return "99+"
    elif cart_len <= 99:
        return cart_len
    
@register.inclusion_tag("gameshop/components/price.html", name="price")
def get_product_price(product):
    return {"product": product}