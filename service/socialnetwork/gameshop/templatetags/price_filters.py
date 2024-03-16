from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter(name="fp")
def format_price(value):
    value = str(value)
    if value == "0":
        return mark_safe("<span class='text-success'>Бесплатно</span>")
    else:
        return f"$ {value}"
