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
from jobs.constants import ValidJobStatus, ValidJobTypes
from model_manager.constants import ModelProvider, OpenAIModels

from diagrams.services.SequenceDiagramService import SequenceDiagramService
from diagrams.repository.SequenceDiagramRepository import SequenceDiagramRepository
from diagrams.services.DiagramExceptions import UMLDiagramCreationError, SequenceDiagramSavingError
from diagrams.services.DiagramConsumerExceptions import SequenceDiagramConsumerError
from diagrams.serializers.CreateSequenceDiagramSerializer import CreateSequenceDiagramSerializer

import logging
logger = logging.getLogger('application_logging')

class SequenceDiagramConsumer(BaseConsumer):
    """
    SequenceDiagramConsumer class that extends the BaseConsumer class.
    Consumes either User Stories OR classes (output from ClassDiagramService) from the JobQueue and generates class diagrams.
    
    Generates ER diagrams using the SequenceDiagramService, and saves the diagrams using the SequenceDiagramRepository.
    args:
        model_provider (ModelProvider): The model provider.
        model_name (Enum): The model name.
        auditor_name (Enum): The auditor name.
        job_id (str): The job ID.
        job_service (JobServiceInterface): The job service. Default is JobService.
        job_queue_service (JobQueueInterface): The job queue service. Default is JobQueueService.
    
    Raises:
        BaseConsumerException: If error encountered while updating the job status or job queue status.
        SequenceDiagramConsumerError: If error encountered while creating the er diagram.
    """    
    def __init__(self, model_provider:ModelProvider, model_name:Enum, 
                 auditor_name:Enum, job_id:str, job_service:JobServiceInterface = JobService(), 
                 job_queue_service:JobServiceInterface = JobQueueService()):    
        
        self.job_id = job_id
        # Initialize the diagram service
        self.diagram_service = SequenceDiagramService(model_provider=model_provider, model_name=model_name, 
                                                   auditor_name=auditor_name, job_id=job_id, serializer_class=CreateSequenceDiagramSerializer)
        # Initialize the repository
        self.repository = SequenceDiagramRepository()

        # Initialize BaseConsumer with the diagram service and repository
        super().__init__(consumer_name="SequenceDiagramConsumer", diagram_service=self.diagram_service, 
                         repository=self.repository, job_service=job_service, job_queue_service=job_queue_service)

         
    def get_specific_error(self, message: str) -> SequenceDiagramConsumerError:
        """
        Returns a SequenceDiagramConsumerError with the specified message.
        args:
            message (str): The error message.
        returns:
            SequenceDiagramConsumerError: The SequenceDiagramConsumerError with the specified
        """
        return SequenceDiagramConsumerError(message)
    
    def create_next_record(self) -> str:
        """
        Following sequence diagram creation, no other jobs will be created.
        """
        logger.info(f"Sequence diagram creation complete. No further jobs to create.")