# bank_project/wsgi.py
import os
from django.core.wsgi import get_wsgi_application

# Points Django to your settings context
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bank_project.settings')

# Exposes the WSGI interface callable for local development and production servers
application = get_wsgi_application()