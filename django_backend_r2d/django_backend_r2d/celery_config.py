from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings
from application_logging.services.application_logging_config import setup_logging
import logging

"""
Celery configuration for Django Backend R2D project.
"""
# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_backend_r2d.settings')

app = Celery('django_backend_r2d')

# Using a string here means the worker will not have to pickle the object when using Windows.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)



setup_logging() # Set up the application logging framework for entire django project 
logger = logging.getLogger('application_logging')