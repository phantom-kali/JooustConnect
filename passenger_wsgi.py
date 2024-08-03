import os
import sys
from importlib import import_module
from django.core.wsgi import get_wsgi_application

# Add the project directory to the system path
sys.path.insert(0, os.path.dirname(__file__))

# Set the default settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jooustconnectprod.settings')

# Import the Django WSGI application
application = get_wsgi_application()

