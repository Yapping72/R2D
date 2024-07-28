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
from diagrams.repository.ClassDiagramRepository import ClassDiagramRepository

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
        
        self.job_id = job_id
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
            er_diagrams (list[dict]): The er diagrams to use.
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
        
        # Iterate over er_diagrams and collect values for each key
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
        
        # Try to retrieve classes, helper_classes and descriptions by checking to see if class_diagrams have already been created
        classes = []
        class_descriptions = []
        helper_classes = []
    
        class_diagrams = self._retrieve_class_diagrams(parent_id) # parent_id is the job_id of er_diagram job
        logger.debug(f"Retrieved class diagrams: {class_diagrams}")
        
        # Iterate over class_diagrams and collect values for each key
        for diagram in class_diagrams:
            if 'classes' in diagram:
                classes.extend(diagram['classes'])
            if 'description' in diagram:
                class_descriptions.append(diagram['description'])
            if 'helper_classes' in diagram:
                helper_classes.extend(diagram['helper_classes'])
                
        # Additional parameters to pass to the next job
        job_parameters = {
            'features': list(set(features)), # Remove duplicated features
            'entities': entities,
            'entity_descriptions': descriptions,
            'classes': list(set(classes)), # Remove duplicated classes  
            'class_descriptions': class_descriptions,
            'helper_classes': list(set(helper_classes)), # Remove duplicated helper classes
            }
            
        logger.debug(f"Job parameters for ER diagram processing: {job_parameters}")
        
        # Create a new job record with parent_id as the job_id, with status as 'Submitted' and type as 'sequence_diagram'
        job = self.create_new_job(parent_job_id=parent_id, job_parameters=job_parameters, 
                                  job_type=job_type, job_status=job_status)
        return job.job_id

    def _retrieve_class_diagrams(self, job_id:str) -> list:
        """
        Attempts to retrieve class diagrams created by parent job of er-diagrams 
        args:
            job_id (str): The er diagram job id 
        returns:
            list[dict]: The class diagrams for the parent job.
        """
        # Checks if this er diagram has an associated parent job with type = class_diagram
        parent_job = self.job_service.get_parent_job(job_id)
        if not parent_job:
            return []
        # Class diagram jobs will be the parent of er diagram jobs 
        class_diagram_repository = ClassDiagramRepository()
        class_diagrams = class_diagram_repository.get_by_id(parent_job.job_id)
        return class_diagrams