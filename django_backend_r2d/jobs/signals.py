from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.db import IntegrityError, OperationalError, DatabaseError
from django.core.exceptions import ValidationError, ObjectDoesNotExist

from jobs.models import Job, JobQueue, JobHistory, JobStatus
from jobs.services.JobExceptions import *   

# Initialize logging class and retrieve the custom user model
import logging
logger = logging.getLogger('application_logging')
from django.contrib.auth import get_user_model
User = get_user_model()

@receiver(post_save, sender=Job)
def add_to_job_queue_on_create(sender, instance, created, **kwargs):
    """
    When a Job is added to Job table, add it to JobQueue if the status is Submitted.
    Raises AddToJobQueueException if an error occurs.
    """
    if created and instance.job_status.code == 3:  # Assuming 3 is the code for "Submitted"
        try:
            JobQueue.objects.create(job=instance, status=instance.job_status, consumer='None')
        except IntegrityError as e:
            logger.error(f"{instance.job_id} has already been submitted")
            raise AddToJobQueueException("Integrity error: " + f"{instance.job_id} has already been submitted")
        except OperationalError as e:
            logger.error(f"Operational error adding job to queue: {e}")
            raise AddToJobQueueException("Operational error: " + str(e))
        except DatabaseError as e:
            logger.error(f"Database error adding job to queue: {e}")
            raise AddToJobQueueException("Database error: " + str(e))
        except ValidationError as e:
            logger.error(f"Validation error adding job to queue: {e}")
            raise AddToJobQueueException("Validation error: " + str(e))
        except Exception as e:
            logger.error(f"Unexpected error adding job to queue: {e}")
            raise AddToJobQueueException("Unexpected error: " + str(e))

@receiver(pre_save, sender=Job)
def add_to_job_queue_on_update(sender, instance, **kwargs):
    """
    When a Job is updated to Submitted state, add it to JobQueue.
    Raises AddToJobQueueException if an error occurs.
    """
    if instance.pk:  # Check if the job already exists (update case)
        try:
            previous = Job.objects.get(pk=instance.pk)
        except ObjectDoesNotExist:
            previous = None
            
        # Check if status changes to Submitted
        if previous and previous.job_status.code != 3 and instance.job_status.code == 3:  
            try:
                JobQueue.objects.create(job=instance, status=instance.job_status, consumer='None')
            except IntegrityError as e:
                logger.error(f"{instance.job_id} has already been submitted")
                raise AddToJobQueueException("Integrity error: " + f"{instance.job_id} has already been submitted")
            except OperationalError as e:
                logger.error(f"Operational error adding job to queue: {e}")
                raise AddToJobQueueException("Operational error: " + str(e))
            except DatabaseError as e:
                logger.error(f"Database error adding job to queue: {e}")
                raise AddToJobQueueException("Database error: " + str(e))
            except ValidationError as e:
                logger.error(f"Validation error adding job to queue: {e}")
                raise AddToJobQueueException("Validation error: " + str(e))
            except Exception as e:
                logger.error(f"Unexpected error adding job to queue: {e}")
                raise AddToJobQueueException("Unexpected error: " + str(e))