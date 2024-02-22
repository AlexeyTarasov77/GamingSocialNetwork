from django.urls import re_path
from .consumers import UserStatusConsumer

websocket_urlpatterns = [
    re_path(r"ws/status/(?P<user_id>\w+)/$", UserStatusConsumer.as_asgi())
]