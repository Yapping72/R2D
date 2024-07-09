from enum import Enum
from celery import shared_task
from diagrams.consumers.ClassDiagramConsumer import ClassDiagramConsumer
import logging
from model_manager.constants import ModelProvider
logger = logging.getLogger('application_logging')
from diagrams.services.DiagramConsumerExceptions import ClassDiagramConsumerError, ClassDiagramTaskError
from framework.consumers.BaseConsumerExceptions import BaseConsumerException

@shared_task
def generate_class_diagram_from_user_stories(model_provider:ModelProvider, model_name:Enum, 
                                             auditor_name:Enum, job_id:str):
    """
    Celery task to generate class diagrams from user stories.
    args:
        model_provider (str or Enum): The model provider.
        model_name (str or Enum): The model name.
        auditor_name (str or Enum): The auditor name.
        job_id (str): The job ID.
    raises:
        ClassDiagramTaskError if an error occurs.
    """
    logger.debug(f"Generating class diagram for - {job_id}")
    try:    
        # Initialize the consumer and process the record
        consumer = ClassDiagramConsumer(model_provider=model_provider, model_name=model_name, 
                                        auditor_name=auditor_name, job_id=job_id)
        # Process the record
        class_diagrams = consumer.process_record(job_id)
        logger.debug(f"Class diagram generated for - {job_id}\nDiagrams:{class_diagrams}")
        
        return class_diagrams
    except (BaseConsumerException, ClassDiagramConsumerError) as e:
        logger.error(f"Error generating class diagram for - {job_id}")
        raise ClassDiagramTaskError(f"Error generating class diagram for - {job_id} - {str(e)}")

    