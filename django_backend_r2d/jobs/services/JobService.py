from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import ValidationError

from jobs.interfaces.JobServiceInterface import JobServiceInterface
from jobs.models import Job
from jobs.serializers.JobSerializer import JobSerializer
from jobs.services.JobExceptions import *

import logging 
logger = logging.getLogger("application_logging") # Instantiate logger class

class JobService(JobServiceInterface):
    """
    Service class for handling Job-related operations.
    Expects a valid user object and job_data dictionary as input.
    """
    def save_job(self, user, job_data):
        """
        Saves a job for the authenticated user. 
        Creates a new job if job_id does not already exist, else updates the existing job.
        """
        job_id = job_data.get('job_id')
        logger.debug(f"{'Creating' if not job_id else 'Updating'} job - {job_data} for user - {user.id}")
        job_data['user'] = user.id  # Add user id to job_data
        try:
            # Check if job_id exists for the user
            if job_id:
                try:
                    # Retrieve job with the provided job_id and user
                    job = Job.objects.get(job_id=job_id, user=user)
                    serializer = JobSerializer(job, data=job_data)
                except Job.DoesNotExist:
                    # If a job with the provided job_id does not exist, create a new job
                    serializer = JobSerializer(data=job_data)  
            else:
                # If job_id is not provided, create a new job
                serializer = JobSerializer(data=job_data)

            if serializer.is_valid():
                # Return the job object if the serializer is valid
                job = serializer.save()
                return job
            else:
                raise ValidationError(serializer.errors)
            
        except ValidationError as e:
            logger.error(f"Validation error {'updating' if job_id else 'creating'} job for user {user.id}: {e}")
            raise JobCreationException(str(e))
        except Exception as e:
            logger.error(f"Error {'updating' if job_id else 'creating'} job for user {user.id}: {e}")
            raise JobCreationException(str(e))
        
    def update_status(self, job_id, status):
        try:
            job = Job.objects.get(job_id=job_id)
            job.job_status = status
            job.save()
            return job
        except ObjectDoesNotExist:
            raise JobNotFoundException(f"Job with id {job_id} does not exist.")

    def delete(self, job_id):
        try:
            job = Job.objects.get(job_id=job_id)
            job.delete()
            return True
        except ObjectDoesNotExist:
            raise JobNotFoundException(f"Job with id {job_id} does not exist.")

    def get_by_id(self, job_id):
        try:
            return Job.objects.get(job_id=job_id)
        except ObjectDoesNotExist:
            raise JobNotFoundException(f"Job with id {job_id} does not exist.")

    def get_all_jobs(self):
        return Job.objects.all()