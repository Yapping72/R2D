"""
WSGI config for django_backend_r2d project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application
from application_logging.services.application_logging_config import setup_logging
import logging


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_backend_r2d.settings')

setup_logging() # Set up the application logging framework for entire django project 
logger = logging.getLogger('application_logging')

application = get_wsgi_application()
logger.info("WSGI application initialized and ready to serve requests.")


