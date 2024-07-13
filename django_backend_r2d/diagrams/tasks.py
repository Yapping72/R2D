from enum import Enum
from celery import shared_task
from diagrams.consumers.ClassDiagramConsumer import ClassDiagramConsumer
import logging
from model_manager.constants import ModelProvider
logger = logging.getLogger('application_logging')
from diagrams.services.DiagramConsumerExceptions import ClassDiagramConsumerError, ClassDiagramTaskError
from framework.consumers.BaseConsumerExceptions import BaseConsumerException
from jobs.constants import ValidJobStatus, ValidJobTypes


@shared_task
def generate_class_diagram_from_user_stories(model_provider:ModelProvider, model_name:Enum, 
                                             auditor_name:Enum, job_id:str) -> str:
    """
    Celery task to generate class diagrams from user stories.
    args:
        model_provider (str or Enum): The model provider.
        model_name (str or Enum): The model name.
        auditor_name (str or Enum): The auditor name.
        job_id (str): The job ID.
    raises:
        ClassDiagramTaskError if an error occurs.
    returns:
        job_id (str): The job ID of the next job record.
        Creates a new job record with parent_id as the job_id, status as 'Submitted' and type as 'er_diagram'.
        This allows for event-driven architecture, where er-diagrams are created after class diagrams are created.
    """
    logger.debug(f"Generating class diagram for - {job_id}")
    try:    
        # Initialize the consumer and process the record
        consumer = ClassDiagramConsumer(model_provider=model_provider, model_name=model_name, 
                                        auditor_name=auditor_name, job_id=job_id)
        # Process the record 
        class_diagrams = consumer.process_record(job_id)  
        logger.info(f"Successfully created class diagram for - {job_id}")
        
        # Create a new job record with parent_id as the job_id, status as 'Submitted' and type as 'er_diagram'
        job_id = consumer.create_next_record(parent_id=job_id, class_diagrams=class_diagrams, 
                                          job_type=ValidJobTypes.ER_DIAGRAM.value, job_status=ValidJobStatus.SUBMITTED.value)
        return job_id
    except (BaseConsumerException, ClassDiagramConsumerError) as e:
        logger.error(f"Error generating class diagram for - {job_id}")
        raise ClassDiagramTaskError(f"Error generating class diagram for - {job_id} - {str(e)}")

    