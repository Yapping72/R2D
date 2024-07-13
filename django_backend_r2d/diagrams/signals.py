from django.db.models.signals import post_save
from django.dispatch import receiver

# Import the Celery tasks to trigger 
from diagrams.tasks import generate_class_diagram_from_user_stories
from diagrams.services.DiagramConsumerExceptions import ClassDiagramConsumerError, ClassDiagramSignalError
from jobs.models import JobQueue
from jobs.constants import ValidJobTypes
from model_manager.models import ModelName
import logging
logger = logging.getLogger('application_logging')

"""
When a JobQueue entry is created with Submitted Status:
1. Check if the job_status is Submitted

If the job_status is submitted:
1. Check if the job_type is class_diagram
2. Trigger the class diagram generation task    
"""

@receiver(post_save, sender=JobQueue)
def trigger_diagram_creation(sender, instance, created, **kwargs):
    """
    Signal receiver that triggers class diagram generation when a JobQueue is created 
    with status Submitted and job_type is class_diagram.

    Args:
        sender (type): The model class that sent the signal (JobQueue).
        instance (JobQueue): The instance of JobQueue that was created or updated.
        created (bool): True if a new instance was created, False if an existing instance was updated.
        **kwargs (dict): Additional keyword arguments.
    Raises:
        ClassDiagramSignalError: If the model information for the JobQueue instance does not exist.
    """
    # Exit if the JobQueue instance is not created or the status is not Submitted
    if not created or instance.status.code != 3:
        return
    
    logger.info(f"Generating {instance.job_type} diagram for Job {instance.job_id}.")
    try:
        # Retrieve job_id and model_information from JobQueue instance
        job_id = instance.job_id
        model_information = ModelName.objects.get(pk=instance.model_id)
        
        if instance.job_type == ValidJobTypes.USER_STORY.value:
            # Add user story generation task here
            pass
        elif instance.job_type == ValidJobTypes.CLASS_DIAGRAM.value:
        # Generate class diagram using the models defined in the JobQueue
            generate_class_diagram_from_user_stories.delay(
                model_provider=model_information.provider,
                model_name=model_information.name,
                auditor_name=model_information.name,
                job_id=job_id,
            )
        elif instance.job_type == ValidJobTypes.ER_DIAGRAM.value:
            # Add ER diagram generation task here
            pass
        elif instance.job_type == ValidJobTypes.SEQUENCE_DIAGRAM.value:
            # Add sequence diagram generation task here
            pass
        elif instance.job_type == ValidJobTypes.STATE_DIAGRAM.value:
            # Add flowchart generation task here
            pass
        else:
            logger.error(f"Invalid job_type: {instance.job_type} for Job {instance.job_id}.")
            raise ClassDiagramSignalError(f"Invalid job_type: {instance.job_type} for Job {instance.job_id}.")
    except ModelName.DoesNotExist:
        logger.error(f"Model information for Job {instance.job_id} does not exist.")
        raise ClassDiagramSignalError(f"Model information: {instance.model_id} not valid for Job: {instance.job_id}")
    except ClassDiagramConsumerError as e:
        logger.error(f"Error generating class diagram for Job {instance.job_id}: {str(e)}")
        raise ClassDiagramSignalError(f"Error generating class diagram for Job {instance.job_id}: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error generating class diagram for Job {instance.job_id}: {str(e)}")
        raise ClassDiagramSignalError(f"Unexpected error generating class diagram for Job {instance.job_id}: {str(e)}")