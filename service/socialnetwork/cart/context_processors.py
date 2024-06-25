from .cart import Cart


def cart(request):
    """Cp for cart to be available in all templates."""
    cart = Cart(request)
    return {"cart": cart}
