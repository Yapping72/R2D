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

from diagrams.services.ERDiagramService import ERDiagramService
from diagrams.repository.ERDiagramRepository import ERDiagramRepository
from diagrams.services.DiagramExceptions import UMLDiagramCreationError, ERDiagramSavingError
from diagrams.services.DiagramConsumerExceptions import ERDiagramConsumerError
from diagrams.serializers.CreateERDiagramSerializer import CreateERDiagramSerializer

import logging
logger = logging.getLogger('application_logging')

class ERDiagramConsumer(BaseConsumer):
    """
    ERDiagramConsumer class that extends the BaseConsumer class.
    Consumes either User Stories OR classes (output from ClassDiagramService) from the JobQueue and generates class diagrams.
    
    Generates ER diagrams using the ERDiagramService, and saves the diagrams using the ERDiagramRepository.
    args:
        model_provider (ModelProvider): The model provider.
        model_name (Enum): The model name.
        auditor_name (Enum): The auditor name.
        job_id (str): The job ID.
        job_service (JobServiceInterface): The job service. Default is JobService.
        job_queue_service (JobQueueInterface): The job queue service. Default is JobQueueService.
    
    Raises:
        BaseConsumerException: If error encountered while updating the job status or job queue status.
        ERDiagramConsumerError: If error encountered while creating the er diagram.
    """    
    def __init__(self, model_provider:ModelProvider, model_name:Enum, 
                 auditor_name:Enum, job_id:str, job_service:JobServiceInterface = JobService(), 
                 job_queue_service:JobServiceInterface = JobQueueService()):    
        
        # Initialize the diagram service
        self.diagram_service = ERDiagramService(model_provider=model_provider, model_name=model_name, 
                                                   auditor_name=auditor_name, job_id=job_id, serializer_class=CreateERDiagramSerializer)
        # Initialize the repository
        self.repository = ERDiagramRepository()

        # Initialize BaseConsumer with the diagram service and repository
        super().__init__(consumer_name="ERDiagramConsumer", diagram_service=self.diagram_service, 
                         repository=self.repository, job_service=job_service, job_queue_service=job_queue_service)

         
    def get_specific_error(self, message: str) -> ERDiagramConsumerError:
        """
        Returns a ERDiagramConsumerError with the specified message.
        args:
            message (str): The error message.
        returns:
            ERDiagramConsumerError: The ERDiagramConsumerError with the specified
        """
        return ERDiagramConsumerError(message)
    
    def create_next_record(self, parent_id:str, er_diagrams:list[dict], 
                           job_type:str=ValidJobTypes.SEQUENCE_DIAGRAM.value, job_status:str=ValidJobStatus.SUBMITTED.value) -> str:
        """
        Creates a new job record for ER diagram processing.
        Passes in the job_id as the parent_id, job_parameters as a list of features, classes and descriptions created and job_type as 'er_diagram'.
        args:  
            parent_id (str): The parent job ID.
            er_diagrams (list[dict]): The class diagrams to use.
            job_type (str): The job type. Default is 'sequence_diagram'.
            job_status (str): The job status. Default is 'Submitted'.
        returns:
            str: The job ID of the new job record.
        """
        logger.debug(f"Creating next job record for ER diagram processing")
        
        # Initialize empty lists to collect the aggregated values
        features = []
        entities = []
        descriptions = []
            
        # Iterate over self.class_diagrams and collect values for each key
        for diagram in er_diagrams:
            if not diagram.get('is_audited'):
                # only retrieve audited diagrams
                continue
            
            if 'feature' in diagram:
                features.extend(diagram['feature'])
            if 'entities' in diagram:
                entities.extend(diagram['entities'])
            if 'description' in diagram:
                descriptions.append(diagram['description'])
            
        job_parameters = {
            'features': list(set(features)), # Remove duplicated features
            'entities': entities,
            'descriptions': descriptions
        }
            
        logger.debug(f"Job parameters for ER diagram processing: {job_parameters}")
        
        # Create a new job record with parent_id as the job_id, with status as 'Submitted' and type as 'er_diagram'
        job = self.create_new_job(parent_job_id=parent_id, job_parameters=job_parameters, 
                                  job_type=job_type, job_status=job_status)
        return job.job_id
