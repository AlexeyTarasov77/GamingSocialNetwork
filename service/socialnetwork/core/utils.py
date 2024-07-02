"""Module with utility functions."""

from django.http import HttpRequest


def is_ajax(request: HttpRequest):
    """Checks does the request is an AJAX request."""
    return (
        request.headers.get("x-requested-with") == "XMLHttpRequest"
        or request.headers.get("Hx-Request") == "true"
    )
