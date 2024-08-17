import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.conf import settings

<<<<<<< HEAD
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "jooustconnectprod.settings")

django_asgi_app = get_asgi_application()
=======
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jooustconnectprod.settings')

django_asgi_app = get_asgi_application()
>>>>>>> 20d5f52ef1d7d03304aa3abc20f5e37cc8590b2c
