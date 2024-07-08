from django.utils import timezone
from django.db import IntegrityError, OperationalError, DatabaseError
from django.core.exceptions import ValidationError, ObjectDoesNotExist

import logging
logger = logging.getLogger('application_logging')

from jobs.models import Job, JobQueue, JobStatus
from jobs.interfaces.JobQueueInterface import JobQueueInterface
from jobs.services.JobExceptions import AddToJobQueueException, RemoveFromJobQueueException, UpdateJobQueueException
from jobs.serializers.UpdateJobQueueStatusSerializer import UpdateJobQueueStatusSerializer

class JobQueueService(JobQueueInterface):
    def enqueue(self, job:Job, consumer:str='None'):
        """
        Adds a job to the JobQueue table.
        args:
            job (Job): The job to add to the queue.
            consumer (str): The consumer to process the job.
            
        raises:
            AddToJobQueueException if an error occurs. 
        """
        try:
            JobQueue.objects.create(
                job=job,
                status=job.job_status,
                job_type=job.job_type,
                model=job.model,
                consumer=consumer
            )
        except IntegrityError as e:
            logger.error(f"{job.job_id} has already been submitted")
            raise AddToJobQueueException("Integrity error: " + f"{job.job_id} has already been submitted")
        except OperationalError as e:
            logger.error(f"Operational error adding job to queue: {e}")
            raise AddToJobQueueException("Operational error: " + str(e))
        except DatabaseError as e:
            logger.error(f"Database error adding job to queue: {e}")
            raise AddToJobQueueException("Database error: " + str(e))
        except ValidationError as e:
            logger.error(f"Validation error adding job to queue: {e}")
            raise AddToJobQueueException("Validation error: " + str(e))
        except Exception as e:
            logger.error(f"Unexpected error adding job to queue: {e}")
            raise AddToJobQueueException("Unexpected error: " + str(e))

    def dequeue(self, job, job_type):
        """
        Removes a job from the JobQueue table.
        Identifies records based on job + job_type
        args:
            job (Job): The job to remove from the queue.
            job_type (str): The type of the job
        raises:
            RemoveFromJobQueueException if an error occurs.
        """
        try:
            JobQueue.objects.filter(job=job, job_type=job_type).delete()
        except JobQueue.DoesNotExist:
            logger.error(f"Job {job.job_id} is not in the queue")
            raise RemoveFromJobQueueException(f"Job {job.job_id} is not in the queue")
        except Exception as e:
            logger.error(f"Unexpected error removing job from queue: {e}")
            raise RemoveFromJobQueueException("Unexpected error: " + str(e))

    def update_status(self, job_id:str, status:str):
        """
        Updates status of a job in job queue
        
        args:
            job_id (str): The job id to update.
            status (str): The status to update.
        
        raises:
            UpdateJobQueueException if an error occurs.
        """
        data = {'job_id': job_id, 'job_status': status}

        try:
            serializer = UpdateJobQueueStatusSerializer(data=data)
            if serializer.is_valid():
                job_queue = JobQueue.objects.get(job_id=job_id)
                job_queue.status = serializer.validated_data['job_status']
                job_queue.save()
            else:
                raise ValidationError(serializer.errors)
        except JobQueue.DoesNotExist:
            logger.error(f"Job {job_id} is not in the queue")
            raise UpdateJobQueueException(f"Job {job_id} is not in the queue")
        except ValidationError as e:
            logger.error(f"Validation error updating job status in queue: {e}")
            raise UpdateJobQueueException(f"Validation error: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error updating job status in queue: {e}")
            raise UpdateJobQueueException(f"Unexpected error: {str(e)}")
