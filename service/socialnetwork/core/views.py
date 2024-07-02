from collections.abc import Callable
from functools import wraps
from logging import Logger
from typing import TypeVar

from django.conf import settings
from django.db import transaction
from django.http import HttpRequest, JsonResponse
from django.http.response import HttpResponse as HttpResponse


def set_logger(logger: Logger):
    global _logger
    _logger = logger


def error_response(exc: Exception, status: int) -> JsonResponse:
    return JsonResponse(
        {"errorMsg": "Unexpected error occured, please try again later: " + str(exc)}, status=status
    )


def handle_exception(exc: Exception):
    assert _logger
    _logger.exception(exc)
    if settings.DEBUG:
        raise exc
    return error_response(exc, 500)


class CatchExceptionMixin:
    """Base class which wraps dispatch into transaction and handles occured exceptions."""
    def dispatch(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        try:
            with transaction.atomic():
                return super().dispatch(request, *args, **kwargs)
        except Exception as e:
            handle_exception(e)


V = TypeVar("V", bound=Callable[..., HttpResponse])


def catch_exception(
    func: V,
) -> V:
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        try:
            with transaction.atomic():
                return func(request, *args, **kwargs)
        except Exception as e:
            handle_exception(e)

    return wrapper
