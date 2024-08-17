"""
WSGI config for jooustconnect project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

<<<<<<< HEAD
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "jooustconnectprod.settings")

application = get_wsgi_application()
=======
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jooustconnectprod.settings')

application = get_wsgi_application()
>>>>>>> 20d5f52ef1d7d03304aa3abc20f5e37cc8590b2c
