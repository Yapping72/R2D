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
from diagrams.services.ClassDiagramService import ClassDiagramService
from diagrams.repository.ClassDiagramRepository import ClassDiagramRepository
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
        
        # Initialize the diagram service
        self.diagram_service = ClassDiagramService(model_provider=model_provider, model_name=model_name, 
                                                   auditor_name=auditor_name, job_id=job_id)
        # Initialize the repository
        self.repository = ClassDiagramRepository()
        
        # Initialize BaseConsumer with the diagram service and repository
        super().__init__(consumer_name="ClassDiagramConsumer",diagram_service=self.diagram_service, 
                         repository=self.repository, job_service=job_service, job_queue_service=job_queue_service)
    
    def get_specific_error(self, message: str) -> ClassDiagramConsumerError:
        """
        Returns a ClassDiagramConsumerError with the specified message.
        args:
            message (str): The error message.
        returns:
            ClassDiagramConsumerError: The ClassDiagramConsumerError with the specified
        """
        return ClassDiagramConsumerError(message)
    
    def create_next_record(self, parent_id:str, class_diagrams:list[dict], 
                           job_type:str=ValidJobTypes.ER_DIAGRAM.value, job_status:str=ValidJobStatus.SUBMITTED.value) -> str:
        """
        Creates a new job record for ER diagram processing.
        Passes in the job_id as the parent_id, job_parameters as a list of features, classes and descriptions created and job_type as 'er_diagram'.
        args:  
            parent_id (str): The parent job ID.
            class_diagrams (list[dict]): The class diagrams to use.
            job_type (str): The job type. Default is 'er_diagram'.
            job_status (str): The job status. Default is 'Submitted'.
        returns:
            str: The job ID of the new job record.
        """
        logger.debug(f"Creating next job record for ER diagram processing")
        
        # Initialize empty lists to collect the aggregated values
        features = []
        classes = []
        descriptions = []
        helper_classes = []
                    
        # Iterate over self.class_diagrams and collect values for each key
        for diagram in class_diagrams:
            if not diagram.get('is_audited'):
                # only retrieve audited diagrams
                continue
            
            if 'feature' in diagram:
                features.extend(diagram['feature'])
            if 'classes' in diagram:
                classes.extend(diagram['classes'])
            if 'description' in diagram:
                descriptions.append(diagram['description'])
            if 'helper_classes' in diagram:
                helper_classes.extend(diagram['helper_classes'])

        job_parameters = {
            'features': list(set(features)),
            'classes': classes,
            'descriptions': descriptions,
            'helper_classes': helper_classes
        }
            
        logger.debug(f"Job parameters for creating ER Diagram Jobs: {job_parameters}")
        # Create a new job record with parent_id as the job_id, with status as 'Submitted' and type as 'er_diagram'
        job = self.create_new_job(parent_job_id=parent_id, job_parameters=job_parameters, 
                                  job_type=job_type, job_status=job_status)
        self.job_service.update_job_description(parent_id, f"Job Completed")
        return job.job_id
