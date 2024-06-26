# jobs/tasks.py
from celery import shared_task
import logging

logger = logging.getLogger('application_logging')

@shared_task
def add(x, y):
    """
    Task to test if celery is working
    """
    logger.debug(f"Adding {x} and {y} in celery")
    return x + y
