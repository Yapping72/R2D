from abc import ABC, abstractmethod
import json 

from jobs.interfaces.JobQueueInterface import JobQueueInterface
from jobs.interfaces.JobServiceInterface import JobServiceInterface
from jobs.services.JobService import JobService
from jobs.services.JobQueueService import JobQueueService
from jobs.services.JobExceptions import JobUpdateException, JobNotFoundException, InvalidJobStatus, UpdateJobQueueException, JobCreationException
from jobs.serializers.UpdateJobStatusSerializer import UpdateJobStatusSerializer
from jobs.models import Job
from jobs.constants import ValidJobStatus
from uuid import uuid4
from framework.consumers.BaseConsumerExceptions import BaseConsumerException, BaseConsumerInitializationException
from diagrams.services.DiagramExceptions import UMLDiagramCreationError
from diagrams.interfaces.BaseDiagramRepository import BaseDiagramRepository
from diagrams.interfaces.BaseDiagramService import BaseDiagramService

from django.contrib.auth import get_user_model
User = get_user_model() # Use custom User model instead of Django default user model

import logging
logger = logging.getLogger('application_logging')

class BaseConsumer(ABC):
    """
    All consumers should inherit from this class, and implement their own create_next_record method.

    The BaseConsumer provides the following functionality:
    - Update the status of a job.
    - Update the status of a job in the job queue.
    - Handle errors by updating job and job queue statuses to Error Failed to Process.
    
    args:
        consumer_name (str): The name of the consumer.
        diagram_service (BaseDiagramService): The diagram service to use.
        repository (BaseDiagramRepository): The repository to use.
        job_service (JobServiceInterface): The job service to use. Uses JobService by default.
        job_queue_service (JobQueueInterface): The job queue service to use. Uses JobQueueService by default.
        diagram_service: The diagram service to use.
        repository: The repository to use.
    raises:
        BaseConsumerException: if error encountered while updating the job status or job queue status.
    """
    def __init__(self, consumer_name: str, diagram_service:BaseDiagramService, 
                 repository:BaseDiagramRepository, job_service:JobServiceInterface = JobService(), 
                 job_queue_service:JobQueueInterface = JobQueueService()):
        # Defines the list of valid consumers
        """
        args:
            consumer_name (str): The name of the consumer. Valid consumers are UserStoryConsumer, ClassDiagramConsumer, ERDiagramConsumer, SequenceDiagramConsumer, StateDiagramConsumer.
            diagram_service (BaseDiagramService): The diagram service to use.
            repository (BaseDiagramRepository): The repository to use.
            job_service (JobServiceInterface): The job service to use. Uses JobService by default.
            job_queue_service (JobQueueInterface): The job queue service to use. Uses JobQueueService by default.
        raises:
            BaseConsumerInitializationException: if invalid job service or job queue service provided.
            BaseConsumerInitializationException: if invalid consumer name provided.
        """
        
        self.valid_consumers = ["UserStoryConsumer", "ClassDiagramConsumer", "ERDiagramConsumer", "SequenceDiagramConsumer", "StateDiagramConsumer"]
        
        if not isinstance(job_service, JobServiceInterface) or not isinstance(job_queue_service, JobQueueInterface):
            raise BaseConsumerInitializationException("Invalid job service or job queue service provided.")
        
        if consumer_name not in self.valid_consumers:
            raise BaseConsumerInitializationException(f"{consumer_name} is not a valid consumer.")
        
        self.consumer_name = consumer_name
        self.job_service = job_service
        self.job_queue_service = job_queue_service
        self.diagram_service = diagram_service
        self.repository = repository 
        self.diagrams = []  # Stores the saved diagrams
        
    def process_record(self, job_id) -> list[dict]:
        """
        Processes the record from the JobQueue and generates  diagrams.
        Saves the class diagrams using the Repository.
        Returns the diagrams that were saved
        
        args: 
            job_id (str): The job ID.
        raises:
            BaseConsumerException: If error encountered while updating the job status or job queue status.
            Concrete ConsumerException: If error encountered while creating diagrams
        
        returns:
            List: List of dictionaries containing the diagrams that were saved.
            Updates the job status and job queue status to Processing or Error Failed to Process.
        """
        try:
            logger.debug(f"Creating diagram for - {job_id}")
            # Update the job status and job queue status to Processing
            self.update_job_status(job_id, ValidJobStatus.PROCESSING.value)
            self.update_job_queue_status(job_id, ValidJobStatus.PROCESSING.value)

            # Generate the diagram using the diagram service
            chain_response = self.diagram_service.generate_diagram()
            
            # Save the diagrams using the diagram repository
            self.diagrams = self.repository.save_diagram(job_id, chain_response)
            
            # Update the job status and job queue status to Completed
            self.update_job_status(job_id, ValidJobStatus.COMPLETED.value)
            self.update_job_queue_status(job_id, ValidJobStatus.COMPLETED.value)
            self.job_service.update_job_description(job_id, f"Job Completed")
            
            return self.diagrams
        except BaseConsumerException as e:
            logger.error(f"Error processing record: {e}")
            self.handle_error(job_id)
            raise BaseConsumerException(f"Error processing record: {e}")
        except UMLDiagramCreationError as e:
            self.handle_error(job_id)
            logger.error(f"Error creating class diagram: {e}")
            raise self.get_specific_error(f"Error encountered while creating diagram: {e}")
        except Exception as e:
            self.handle_error(job_id)
            logger.error(f"Unhandled Error processing record: {e}")
            raise self.get_specific_error(f"Error encountered while creating diagram: {e}")
    
    @abstractmethod
    def get_specific_error(self, message: str):
        """
        Returns a specific error to raise
        
        args:
            message (str): The error message.
        returns:
            Specific error to raise
        """
        pass 
        
    @abstractmethod
    def create_next_record(self) -> Job:
        """
        Create the next record to process.
        Concrete classes should implement this method to create the next record to process. 
        Concrete classes should invoke the create_new_job method to create a new job record.
        """
        pass 

    def create_new_job(self, parent_job_id: str, job_parameters:dict, job_type:str, job_status:str) -> Job:
        """
        Creates a new job record with parent_id as the job_id, status as 'Submitted' and the given job type.
        Stores the newly created job record in the Jobs table, a corresponding JobQueue record will be created via Signals.
        Concrete classes should invoke this method in their create_next_record method.
        If a job is successfully created with status submitted, the parent_job's status will be set to 'Processing'.
        
        args:
            parent_job_id (str): The job ID.
            job_parameters (dict): The job parameters.
            job_type (str): The job type.
            job_status (str): The job status.
        returns:
            Job: The created job record.
        """
        
        # Retrieve user and model for the associated parent job
        parent_job = self.job_service.get_job_by_id(parent_job_id)
        logger.debug(f"fetched parent job {parent_job} for creating new job")
       
        # Extract necessary fields from serialized data
        user_id = parent_job['user']
        model_name = parent_job['model_name']

        # Retrieve the actual user instance
        user = User.objects.get(id=user_id)
        
        new_job_data = {
            'job_id': str(uuid4()),
            'user': user, 
            'parent_job': parent_job_id, # Set the newly created job's parent_id to the parent job_id provided
            'parameters': json.dumps(job_parameters),
            'job_type': job_type,
            'job_status': job_status,
            'job_details': f"{job_type} job created by {parent_job_id}",
            'model_name': model_name
        }
        try:
            # Try to save the a new job record
            job = self.job_service.save_job(user, new_job_data)
            # If a child job is successfully created with status submitted, set the parent_job's status to 'Processing'
            if job is not None:
                # Update the parent job status to Processing
                self.update_job_status(parent_job_id, ValidJobStatus.PROCESSING.value)
            return job
        except JobCreationException as e:
            raise BaseConsumerException(f"Error creating new job record for {job_type}: {str(e)}")
        except BaseConsumerException as e:  
            raise BaseConsumerException(f"Failed to update parent job to processing {parent_job_id}: {str(e)}")
        except Exception as e:
            raise BaseConsumerException(f"Unhandled exception occurred while trying to create new job record: {str(e)}")
     
    def update_job_status(self, job_id:str, job_status:str):
        """
        Update the status of a job.
        args:
            job_id (str): The job id to update.
            job_status (str): The name of the status to update.
        raises:
            BaseConsumerExceptions: if error encountered while updating the job status.
            
        valid job_status: Draft, Queued, Submitted, Error Failed to Submit, Processing, Error Failed to Process, Job Aborted, Completed
        """ 
        try: 
            self.job_service.update_status_by_id(job_id, job_status)
            logger.debug(f"Job status for job {job_id} updated to {job_status}")
        except (JobUpdateException, JobNotFoundException, InvalidJobStatus) as e:
            logger.error(f"Error updating job status: {str(e)}")
            raise BaseConsumerException(f"Error updating job status: {str(e)}")
        except Exception as e:
            logger.error(f"Unhandled exception occurred while trying to update job status: {str(e)}")
            raise BaseConsumerException(f"Unhandled exception occurred while trying updating job status: {str(e)}")
        
    def update_job_queue_status(self, job_id:str, job_status:str):
        """
        Update the status of the job in the job queue.
        args:
            job_id (str): The job id to update.
            job_status (str): The name of the status to update.
        raises:
            BaseConsumerExceptions: if error encountered while updating the job status in job queue
            
        valid job_status: Submitted, Processing, Error Failed to Process, Job Aborted, Completed
        """
        try:
            self.job_queue_service.update_status(job_id=job_id, status=job_status, consumer=self.consumer_name)
            logger.debug(f"Job queue status for job {job_id} updated to {job_status} for consumer {self.consumer_name}")
        except UpdateJobQueueException as e:
            logger.error(f"Error updating job queue status: {str(e)}")
            raise BaseConsumerException(f"Error updating job queue status: {str(e)}")
        except Exception as e:
            logger.error(f"Unhandled exception occurred while trying updating job queue status: {str(e)}")
            raise BaseConsumerException(f"Unhandled exception occurred while trying updating job queue status: {str(e)}")
        
    def handle_error(self, job_id):
        """
        Handle errors by updating job and job queue statuses to Error Failed to Process.
        
        Args:
            job_id (str): The job ID.
        
        Attempts to update the job status and job queue status to Error Failed to Process, will manually update the job and job queue status if the update fails.
        """
        try:
            # Try to update the job status to Error Failed to Process
            self.update_job_status(job_id, ValidJobStatus.ERROR_FAILED_TO_PROCESS.value)
        except BaseConsumerException as e:
            logger.error(f"Failed to update job status to Error Failed to Process: {str(e)}")
            raise BaseConsumerException(f"Failed to update job status to Error Failed to Process: {str(e)}")
        except Exception as e:
            raise BaseConsumerException(f"Unhandled exception occurred while trying to update job status to Error Failed to Process: {str(e)}")

        try:
            # Try to update the job status to Error Failed to Process
            self.update_job_queue_status(job_id, ValidJobStatus.ERROR_FAILED_TO_PROCESS.value)
        except BaseConsumerException as e:
            logger.error(f"Failed to update job queue status to Error Failed to Process: {str(e)}")
            raise BaseConsumerException(f"Failed to update job queue status to Error Failed to Process: {str(e)}")
        except Exception as e:
            raise BaseConsumerException(f"Unhandled exception occurred while trying to update job queue status to Error Failed to Process: {str(e)}")

    def complete_all_jobs(self, job_id:str):
        """
        The final consumer should invoke this function. 
        It will set the status of all parent jobs to Completed.
        """
        try:
            # Update the status of all parent jobs to Completed
            self.job_service.update_all_parent_jobs_as_completed(job_id)
        except (JobNotFoundException, JobUpdateException) as e:
            logger.error(f"Error updating all parent jobs to Completed: {str(e)}")
            raise BaseConsumerException(f"Error updating all parent jobs to Completed: {str(e)}")
