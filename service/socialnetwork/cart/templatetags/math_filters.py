from django.template import Library

register = Library()

@register.filter
def mul(value, arg):
    return value * arg