from django.http import HttpResponseForbidden, HttpResponseServerError
from django.shortcuts import get_object_or_404, redirect
from orders.models import Order
from users.models import Profile

def owner_required(app_name):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            try:
                user = request.user
                err = HttpResponseForbidden()
                match app_name:
                    case "users": obj = get_object_or_404(Profile, user_slug=kwargs["username"])
                    case "orders": obj = get_object_or_404(Order, id=kwargs["order_id"])
                if user != obj.user: return err
                return view_func(request, *args, **kwargs)
            except Exception as e:
                print(e)
                return HttpResponseServerError()

        return wrapper

    return decorator
