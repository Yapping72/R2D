from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.db import IntegrityError, OperationalError, DatabaseError
from django.core.exceptions import ValidationError, ObjectDoesNotExist

from jobs.models import Job, JobQueue, JobHistory, JobStatus
from jobs.services.JobExceptions import *   
from jobs.services.JobQueueService import JobQueueService

# Initialize logging class and retrieve the custom user model
import logging
logger = logging.getLogger('application_logging')
from django.contrib.auth import get_user_model
User = get_user_model()

# Class responsible for updating JobQueue when a Job is created or updated 
job_queue_service = JobQueueService()

# Import the Celery tasks to trigger 
from model_manager.constants import ModelProvider, OpenAIModels
from model_manager.models import ModelName
from diagrams.tasks import generate_class_diagram_from_user_stories

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
        
# add Job to JobQueue when a Job is updated to Submitted
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

"""
Class diagram generation will be triggered when a JobQueue is created with:
1. status Submitted and job_type is class_diagram
"""
# Create class diagram when a JobQueue is created with status Submitted and job_type is class_diagram
@receiver(post_save, sender=JobQueue)
def trigger_class_diagram(sender, instance, created, **kwargs):
    if created and instance.job.job_status.code == 3 and instance.job_type == "class_diagram":
        # Retrieve the model provider and model name based on the JobQueue Model
        model = ModelName.objects.get(id=instance.model)
        generate_class_diagram_from_user_stories.delay(instance.job_id)