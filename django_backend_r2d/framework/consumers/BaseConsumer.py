from abc import ABC, abstractmethod

from jobs.interfaces.JobQueueInterface import JobQueueInterface
from jobs.interfaces.JobServiceInterface import JobServiceInterface
from jobs.services.JobService import JobService
from jobs.services.JobQueueService import JobQueueService
from jobs.serializers.UpdateJobStatusSerializer import UpdateJobStatusSerializer
from jobs.services.JobExceptions import JobUpdateException, JobNotFoundException, InvalidJobStatus, UpdateJobQueueException
from jobs.constants import ValidJobStatus

from framework.consumers.BaseConsumerExceptions import BaseConsumerException, BaseConsumerInitializationException

import logging
logger = logging.getLogger('application_logging')

class BaseConsumer(ABC):
    """
    All consumers should inherit from this class, and implement their own process_record method.

    The BaseConsumer provides the following functionality:
    - Update the status of a job.
    - Update the status of a job in the job queue.
    - Handle errors by updating job and job queue statuses to Error Failed to Process.
    
    args:
        consumer_name (str): The name of the consumer.
        job_service (JobServiceInterface): The job service to use. Uses JobService by default.
        job_queue_service (JobQueueInterface): The job queue service to use. Uses JobQueueService by default.
    
    raises:
        BaseConsumerException: if error encountered while updating the job status or job queue status.
    """
    def __init__(self, consumer_name: str, job_service:JobServiceInterface = JobService(), job_queue_service:JobQueueInterface = JobQueueService()):
        # Defines the list of valid consumers
        
        self.valid_consumers = ["UserStoryConsumer", "ClassDiagramConsumer", "ERDiagramConsumer"]
        if not isinstance(job_service, JobServiceInterface) or not isinstance(job_queue_service, JobQueueInterface):
            raise BaseConsumerInitializationException("Invalid job service or job queue service provided.")
        
        if consumer_name not in self.valid_consumers:
            raise BaseConsumerInitializationException("{consumer_name} is not a valid consumer.")
        
        self.consumer_name = consumer_name
        self.job_service = job_service
        self.job_queue_service = job_queue_service
    
    @abstractmethod
    def process_record(self, record: dict) -> dict:
        """
        Process a record and return the result.
        
        :param record: The record to process
        :return: The result of processing the record
        """
        pass
    
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
        except (JobUpdateException, JobNotFoundException, InvalidJobStatus) as e:
            logger.error(f"Error updating job status: {e}")
            raise BaseConsumerException(f"Error updating job status: {e}")
        except Exception as e:
            logger.error(f"Unhandled exception occurred while trying updating job status: {e}")
            raise BaseConsumerException(f"Unhandled exception occurred while trying updating job status: {e}")
        
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
            self.job_queue_service.update_status(job, job_status)
        except UpdateJobQueueException as e:
            logger.error(f"Error updating job queue status: {e}")
            raise BaseConsumerException(f"Error updating job queue status: {e}")
        except Exception as e:
            logger.error(f"Unhandled exception occurred while trying updating job queue status: {e}")
            raise BaseConsumerException(f"Unhandled exception occurred while trying updating job queue status: {e}")
        
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
            logger.error(f"Failed to update job status to Error Failed to Process: {e}")
            raise BaseConsumerException(f"Failed to update job status to Error Failed to Process: {e}")
        except Exception as e:
            raise BaseConsumerException(f"Unhandled exception occurred while trying to update job status to Error Failed to Process: {e}")

        try:
            # Try to update the job status to Error Failed to Process
            self.update_job_queue_status(job_id, ValidJobStatus.ERROR_FAILED_TO_PROCESS.value)
        except BaseConsumerException as e:
            logger.error(f"Failed to update job queue status to Error Failed to Process: {e}")
            raise BaseConsumerException(f"Failed to update job queue status to Error Failed to Process: {e}")
        except Exception as e:
            raise BaseConsumerException(f"Unhandled exception occurred while trying to update job queue status to Error Failed to Process: {e}")