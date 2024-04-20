from django.http import HttpResponseForbidden, HttpResponseServerError
from django.shortcuts import get_object_or_404, redirect
from orders.models import Order
from users.models import Profile

# def owner_required(view_func):
#     def wrapper_func(request, *args, **kwargs):
#         profile = get_object_or_404(Profile, user_slug=kwargs["username"])
#         if request.user == profile.user:
#             return view_func(request, *args, **kwargs)
#         else:
#             return HttpResponseForbidden()
#     return wrapper_func


def owner_required(app_name):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            try:
                user = request.user
                err = HttpResponseForbidden()
                match app_name:
                    case "users":
                        profile = get_object_or_404(
                            Profile, user_slug=kwargs["username"]
                        )
                        if user != profile.user:
                            return err
                    case "orders":
                        order = get_object_or_404(Order, id=kwargs["order_id"])
                        if user != order.user:
                            return err
                return view_func(request, *args, **kwargs)
            except Exception as e:
                return HttpResponseServerError()

        return wrapper

    return decorator
