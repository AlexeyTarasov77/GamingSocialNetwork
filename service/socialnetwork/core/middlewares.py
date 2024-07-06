import logging

from django.http import JsonResponse

logger = logging.getLogger(__name__)


class HandleExceptionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_exception(self, request, exception) -> JsonResponse:
        logger.exception(exception)
        return JsonResponse({
            "success": False,
            "errorMsg": "Unexpected error occured, please try again later: " + str(exception),
        })
