#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import logging
from application_logging.services.application_logging_config import setup_logging, flush_cloudwatch_handler
import logging

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_backend_r2d.settings')
    try: 
        from django.core.management import execute_from_command_line
        setup_logging() # Set up the application logging framework for entire django project 
        logger = logging.getLogger('application_logging')
        logger.debug("Django management command started.")
        # Flush the CloudWatch handler to ensure logs are delivered
        flush_cloudwatch_handler()
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
