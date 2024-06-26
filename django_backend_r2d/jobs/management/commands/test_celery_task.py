# jobs/management/commands/test_celery_task.py
from django.core.management.base import BaseCommand
from jobs.tasks import add
import logging

# R2D Logger module
logger = logging.getLogger('application_logging')

class Command(BaseCommand):
    help = 'Test Celery task'

    def handle(self, *args, **kwargs):
        result = add.delay(4, 6)
        self.stdout.write(f"Task ID: {result.id}")
        self.stdout.write(f"Result: {result.get(timeout=10)}")
        logger.debug(f"Task ID: {result.id}")
        logger.debug(f"Result: {result.get(timeout=10)}")
