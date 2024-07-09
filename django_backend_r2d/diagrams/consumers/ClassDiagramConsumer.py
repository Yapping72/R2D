from enum import Enum
from django.core.exceptions import ObjectDoesNotExist
from framework.consumers.BaseConsumer import BaseConsumer
from framework.consumers.BaseConsumerExceptions import BaseConsumerException
from jobs.models import JobQueue, Job, JobStatus
from jobs.interfaces.JobServiceInterface import JobServiceInterface
from jobs.interfaces.JobQueueInterface import JobQueueInterface
from jobs.services.JobService import JobService
from jobs.services.JobQueueService import JobQueueService
from jobs.services.JobExceptions import JobNotFoundException
from jobs.constants import ValidJobStatus
from model_manager.constants import ModelProvider, OpenAIModels
from diagrams.services.ClassDiagramService import ClassDiagramService
from diagrams.services.ClassDiagramRepository import ClassDiagramRepository
from diagrams.services.DiagramExceptions import UMLDiagramCreationError, ClassDiagramSavingError
from diagrams.services.DiagramConsumerExceptions import ClassDiagramConsumerError

import logging
logger = logging.getLogger('application_logging')

class ClassDiagramConsumer(BaseConsumer):
    """
    ClassDiagramConsumer class that extends the BaseConsumer class.
    Consumes User Stories from the JobQueue and generates class diagrams.
    
    Generates class diagrams using the ClassDiagramService, and saves the diagrams using the ClassDiagramRepository.
    args:
        model_provider (ModelProvider): The model provider.
        model_name (Enum): The model name.
        auditor_name (Enum): The auditor name.
        job_id (str): The job ID.
        job_service (JobServiceInterface): The job service. Default is JobService.
        job_queue_service (JobQueueInterface): The job queue service. Default is JobQueueService.
    
    Raises:
        BaseConsumerException: If error encountered while updating the job status or job queue status.
        ClassDiagramConsumerError: If error encountered while creating the class diagram.
    """    
    def __init__(self, model_provider:ModelProvider, model_name:Enum, 
                 auditor_name:Enum, job_id:str, job_service:JobServiceInterface = JobService(), 
                 job_queue_service:JobServiceInterface = JobQueueService()):    
        super().__init__(consumer_name="ClassDiagramConsumer", job_service=job_service, job_queue_service=job_queue_service)
        # Initialize the diagram service
        self.diagram_service = ClassDiagramService(model_provider=model_provider, model_name=model_name, 
                                                   auditor_name=auditor_name, job_id=job_id)
        self.repository = ClassDiagramRepository()
        
    def process_record(self, job_id) -> dict:
        """
        Processes the record from the JobQueue and generates class diagrams.
        Saves the class diagrams using the ClassDiagramRepository.
        Returns the class diagrams that were saved
        args: 
            job_id (str): The job ID.
        raises:
            BaseConsumerException: If error encountered while updating the job status or job queue status.
            ClassDiagramConsumerError: If error encountered while creating the class diagram.
        
        returns:
            dict: The class diagrams that were saved.
            Updates the job status and job queue status to Processing or Error Failed to Process.
        """
        try:
            logger.debug(f"Creating class diagram for - {job_id}")
            # Update the job status and job queue status to Processing
            self.update_job_status(job_id, ValidJobStatus.PROCESSING.value)
            self.update_job_queue_status(job_id, ValidJobStatus.PROCESSING.value)

            # Generate the class diagram using the diagram service
            chain_response = self.diagram_service.generate_diagram()
            # Save the class diagrams using the diagram repository
            class_diagrams = self.repository.save_diagram(job_id, chain_response)
            
            # Update the job status and job queue status to Completed
            self.update_job_status(job_id, ValidJobStatus.COMPLETED.value)
            self.update_job_queue_status(job_id, ValidJobStatus.COMPLETED.value)
            
            return class_diagrams
        except BaseConsumerException as e:
            logger.error(f"Error processing record: {e}")
            self.handle_error(job_id)
            raise BaseConsumerException(f"Error processing record: {e}")
        except UMLDiagramCreationError as e:
            self.handle_error(job_id)
            logger.error(f"Error creating class diagram: {e}")
            raise ClassDiagramConsumerError(f"Error encountered while creating class diagram: {e}")
        except Exception as e:
            self.handle_error(job_id)
            logger.error(f"Unhandled Error processing record: {e}")
            raise ClassDiagramConsumerError(f"Unhandled Error encountered while processing record: {e}")    

