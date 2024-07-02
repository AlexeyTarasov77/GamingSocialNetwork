from channels.routing import URLRouter
from chats.routing import websocket_urlpatterns as chats_websocket_urlpatterns
from django.urls import re_path
from gameblog.routing import websocket_urlpatterns as gameblog_websocket_urlpatterns

websocket_urlpatterns = URLRouter([
    re_path(r"ws/chats/", URLRouter(chats_websocket_urlpatterns)),
    re_path(r"ws/gameblog/", URLRouter(gameblog_websocket_urlpatterns)),
])
