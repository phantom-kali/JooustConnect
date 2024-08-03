import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jooustconnectprod.settings')

django_asgi_app = get_asgi_application()