from decimal import Decimal
from django.http import HttpRequest

class Cart():
    def __init__(self, request: HttpRequest) -> None:
        self.session = request.session
        cart = self.session.get("session_key")
        if not cart: # если сессия еще не существует - инициализиовать ее пустым обьектом
            cart = self.session["session_key"] = {} 
        self.cart = cart