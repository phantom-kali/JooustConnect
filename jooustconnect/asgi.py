import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jooustconnect.settings')

django_asgi_app = get_asgi_application()

from socialapp import routing  # Import routing after Django setup

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AuthMiddlewareStack(
        URLRouter(
            routing.websocket_urlpatterns
        )
    ),
})