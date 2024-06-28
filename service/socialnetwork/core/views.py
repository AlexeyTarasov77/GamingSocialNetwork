from functools import wraps
from django.db import transaction
from django.http import HttpRequest, JsonResponse
from django.http.response import HttpResponse as HttpResponse
from django.views.generic import View
from django.conf import settings
from logging import Logger


def set_logger(logger: Logger):
    global _logger
    _logger = logger


def error_response(exc, status):
    return JsonResponse({"errorMsg": str(exc)}, status=status)


def handle_exception(exc):
    _logger.exception(exc)
    if settings.DEBUG:
        raise exc
    return error_response(exc, 500)


class BaseView(View):
    def dispatch(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        print("Dispatching")
        try:
            with transaction.atomic():
                return super().dispatch(request, *args, **kwargs)
        except Exception as e:
            handle_exception(e)


def base_view(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        try:
            with transaction.atomic():
                return func(request, *args, **kwargs)
        except Exception as e:
            handle_exception(e)

    return wrapper
