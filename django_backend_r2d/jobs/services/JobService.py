from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import ValidationError

from jobs.interfaces.JobServiceInterface import JobServiceInterface
from jobs.models import Job, JobStatus
from jobs.serializers.JobSerializer import JobSerializer
from jobs.serializers.UpdateJobStatusSerializer import UpdateJobStatusSerializer
from jobs.serializers.GetJobSerializer import GetJobSerializer
from jobs.services.JobExceptions import *

import logging 
logger = logging.getLogger("application_logging") # Instantiate logger class

class JobService(JobServiceInterface):
    """
    JobService class that implements the JobServiceInterface.
    Provides methods to create, update and retrieve jobs.
    """
    def save_job(self, user, job_data:dict):
        """
        Saves a job for the authenticated user.
        Creates a new job if job_id does not already exist, else updates the existing job.

        Args:
            user: The authenticated user.
            job_data (dict): The job data to save.

        Returns:
            Job: The saved or updated job object.

        Raises:
            JobCreationException: If there is an error creating or updating the job.
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
                logger.error(f"Serializer validation error for job data {job_data} with errors: {serializer.errors}")
                raise ValidationError(serializer.errors)
            
        except ValidationError as e:
            logger.error(f"Validation error {'updating' if job_id else 'creating'} job for user {user.id}: {e}")
            raise JobCreationException(e.detail)
        except Exception as e:
            logger.error(f"Error {'updating' if job_id else 'creating'} job for user {user.id}: {e}")
            raise JobCreationException(str(e))
        
    def update_status(self, user, job_data):
        """
        Updates the status of a job.

        Args:
            user: The authenticated user.
            job_data (dict): The job data with the new status.

        Returns:
            Job: The updated job object.

        Raises:
            ValidationError: If the job data is invalid.
            JobNotFoundException: If the job does not exist.
            InvalidJobStatus: If the job status is invalid.
        """
        serializer = UpdateJobStatusSerializer(data=job_data)
        # Raise an error if serializer is not valid
        if not serializer.is_valid():
            logger.error(f"Serializer validation error for job data {job_data} with errors: {serializer.errors}")
            raise ValidationError(serializer.errors)

        # Retrieve the validated job_id and job_status from the serializer
        job_id = serializer.validated_data.get('job_id')
        job_status = serializer.validated_data.get('job_status')

        try:
            job = Job.objects.get(job_id=job_id, user=user)
            job_status_instance = JobStatus.objects.get(name=job_status)
            job.job_status = job_status_instance
            job.save() 
            return job
        except Job.DoesNotExist:
            raise JobNotFoundException(f"Job with id {job_id} does not exist for user {user.id}.")
        except JobStatus.DoesNotExist:
            raise InvalidJobStatus(f"Invalid job status: {job_status}")
        except Exception as e:
            logger.error(f"Error updating job status for job_id {job_id} for user {user.id}: {e}")
            raise JobUpdateException(str(e))
        
    def get_job_for_user(self, user, request_payload):
        """
        Retrieves a specific job for a user by job_id.

        Args:
            user: The authenticated user.
            request_payload (dict): The request payload containing the job_id.

        Returns:
            dict: The job data.

        Raises:
            ValidationError: If the request payload is invalid.
            JobNotFoundException: If the job does not exist.
        """
        
        request_payload['user'] = user.id  # Ensure user field is included in the payload
        serializer = GetJobSerializer(data=request_payload)
        if not serializer.is_valid():
            logger.error(f"Serializer validation error for payload {request_payload} with errors: {serializer.errors}")
            raise ValidationError(serializer.errors)

        validated_data = serializer.validated_data
        
        try:
            job = Job.objects.get(job_id=validated_data['job_id'], user=user)
            return JobSerializer(job).data # Serialize the job object
        except Job.DoesNotExist:
            raise JobNotFoundException(f"Job with id {validated_data['job_id']} does not exist for user {user.id}.")

    def get_all_jobs_for_user(self, user):
        """
        Retrieves all jobs for a given user.

        Args:
            user: The authenticated user.

        Returns:
            list: A list of all jobs for the user.
        """
        jobs = Job.objects.filter(user=user)
        logger.debug(f"Retrieved {jobs} jobs for user {user.id}")
        return JobSerializer(jobs, many=True).data # Serialize the job objects

    def get_job_by_id(self, job_id):
        """
        Retrieves a job by its job_id.

        Args:
            job_id (str): The job ID.

        Returns:
            dict: The job data.

        Raises:
            JobNotFoundException: If the job does not exist.
        """
        try:
            job = Job.objects.get(job_id = job_id)
            return JobSerializer(job).data # Serialize the job object
        except Job.DoesNotExist:
            raise JobNotFoundException(f"Job with id {validated_data['job_id']} does not exist for user {user.id}.")

        
