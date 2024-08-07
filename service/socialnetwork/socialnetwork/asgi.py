"""
ASGI config for socialnetwork project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application
from socialnetwork.routing import websocket_urlpatterns

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "socialnetwork.settings")

django_application = get_asgi_application()

application = ProtocolTypeRouter({
    "http": django_application,
    "websocket": AllowedHostsOriginValidator(AuthMiddlewareStack(websocket_urlpatterns)),
})
