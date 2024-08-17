import os
import sys
from importlib import import_module
from django.core.wsgi import get_wsgi_application

# Add the project directory to the system path
sys.path.insert(0, os.path.dirname(__file__))

# Set the default settings module
<<<<<<< HEAD
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "jooustconnectprod.settings")

# Import the Django WSGI application
application = get_wsgi_application()
=======
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jooustconnectprod.settings')

# Import the Django WSGI application
application = get_wsgi_application()

>>>>>>> 20d5f52ef1d7d03304aa3abc20f5e37cc8590b2c
