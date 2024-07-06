from django.utils import timezone
from django.db import IntegrityError, OperationalError, DatabaseError
from django.core.exceptions import ValidationError, ObjectDoesNotExist

import logging
logger = logging.getLogger('application_logging')

from jobs.models import Job, JobQueue, JobStatus
from jobs.interfaces.JobQueueInterface import JobQueueInterface
from jobs.services.JobExceptions import *

class JobQueueService(JobQueueInterface):
    def enqueue(self, job, status, consumer='None'):
        """
        Adds a job to the JobQueue table.
        Raises AddToJobQueueException if an error occurs. 
        """
        try:
            JobQueue.objects.create(job=job, status=status, consumer=consumer)
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

    def dequeue(self, job):
        """
        Removes a job from the JobQueue table.
        Raises RemoveFromJobQueueException if an error occurs.
        """
        try:
            JobQueue.objects.filter(job=job).delete()
        except JobQueue.DoesNotExist:
            logger.error(f"Job {job.job_id} is not in the queue")
            raise RemoveFromJobQueueException(f"Job {job.job_id} is not in the queue")
        except Exception as e:
            logger.error(f"Unexpected error removing job from queue: {e}")
            raise RemoveFromJobQueueException("Unexpected error: " + str(e))

    def update_status(self, job, status):
        """
        Updates status of a job in job queue
        Raises UpdateJobQueueException if an error occurs.
        """
        try:
            job_queue = JobQueue.objects.get(job=job)
            job_queue.status = status
            job_queue.save()
        except JobQueue.DoesNotExist:
            logger.error(f"Job {job.job_id} is not in the queue")
            raise UpdateJobQueueException(f"Job {job.job_id} is not in the queue")
        except Exception as e:
            logger.error(f"Unexpected error updating job status in queue: {e}")
            raise UpdateJobQueueException("Unexpected error: " + str(e))

