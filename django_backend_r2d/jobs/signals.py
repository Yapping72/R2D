from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.db import IntegrityError, OperationalError, DatabaseError
from django.core.exceptions import ValidationError, ObjectDoesNotExist

from jobs.models import Job, JobQueue, JobHistory, JobStatus
from jobs.services.JobExceptions import *   
from jobs.services.JobQueueService import JobQueueService
from jobs.services.JobHistoryService import JobHistoryService

# Initialize logging class and retrieve the custom user model
import logging
logger = logging.getLogger('application_logging')
from django.contrib.auth import get_user_model
User = get_user_model()

# Class responsible for updating JobQueue when a Job is created or updated 
job_queue_service = JobQueueService()

"""
A Job will be added to JobQueue if:
1. It is created with status Submitted
2. It is updated to status Submitted
"""
# Add Job to JobQueue when a Job is created with status Submitted
@receiver(post_save, sender=Job)
def add_to_job_queue_on_create(sender, instance, created, **kwargs):
    """
    When a Job is added to Job table, add it to JobQueue if the status is Submitted.
    Raises AddToJobQueueException if an error occurs.
    """
    if created and instance.job_status.code == 3:  # Check if the job is created and status is Submitted
        job_queue_service.enqueue(job=instance)
        
# Add Job to JobQueue when a Job is updated to Submitted
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
            job_queue_service.enqueue(job=instance)

# Add a JobHistory entry when a Job is created
@receiver(post_save, sender=Job)
def create_job_history_on_create(sender, instance, created, **kwargs):
    if created:  # Job creation
        user = instance.user if hasattr(instance, 'user') else None
        try:
            JobHistoryService.log_job_history(
                job=instance,
                user=user,
                previous_status=None,  # No previous status for new job
                current_status=instance.job_status
            )
            logger.debug(f"Job history logged for Job ID {instance.job_id}: {instance.job_status}")
        except Exception as e:
            logger.error(f"Failed to log job history for Job ID {instance.job_id}: {str(e)}")

# Add a JobHistory entry when a Job is updated
@receiver(pre_save, sender=Job)
def create_job_history_on_status_change(sender, instance, **kwargs):
    if instance.pk:  # Check if the job already exists (update case)
        try:
            previous = Job.objects.get(pk=instance.pk)
        except ObjectDoesNotExist:
            previous = None

        if previous and previous.job_status != instance.job_status:
            user = instance.user if hasattr(instance, 'user') else None
            try:
                # Log job history for status change
                JobHistoryService.log_job_history(
                    job=instance,
                    user=user,
                    previous_status=previous.job_status,
                    current_status=instance.job_status
                )
                logger.debug(f"Job history logged for Job ID {instance.job_id} from {previous.job_status} to {instance.job_status}")
            except Exception as e:
                logger.error(f"Failed to log job history for Job ID {instance.job_id}: {str(e)}")
                # Do not raise exception so that the job is not affected by history logging failure