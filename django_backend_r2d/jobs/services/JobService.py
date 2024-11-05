from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import ValidationError

from jobs.interfaces.JobServiceInterface import JobServiceInterface
from jobs.models import Job, JobStatus
from jobs.serializers.JobSerializer import JobSerializer
from jobs.serializers.UpdateJobStatusSerializer import UpdateJobStatusSerializer
from jobs.serializers.GetJobSerializer import GetJobSerializer
from jobs.services.JobExceptions import *
from jobs.constants import ValidJobStatus

import logging 
logger = logging.getLogger("application_logging") # Instantiate logger class

class JobService(JobServiceInterface):
    """
    JobService class that implements the JobServiceInterface.
    Provides methods to create, update and retrieve jobs.
    """
    def save_job(self, user, job_data:dict) -> Job:
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
        job_data['user'] = user.id  # Add user id to job_data

        try:
            try:
                # Try to retrieve the job if it already exists -- Update Case
                job = Job.objects.get(job_id=job_id, user=user)
                serializer = JobSerializer(job, data=job_data)
            except Job.DoesNotExist:
                # Create a new job if it does not exist -- Create Case
                serializer = JobSerializer(data=job_data)
            
            if serializer.is_valid():
                # Save the job if the serializer is valid
                job = serializer.save()
                logger.debug(f"Job record Successfully saved for user {user.id}")
                return job
            
            # Log and raise validation error if serializer is invalid
            logger.error(f"Failed to save job due to invalid job data - {serializer.errors} for job_id {job_id} for user {user.id}")
            raise ValidationError(serializer.errors)
            
        except ValidationError as e:
            logger.error(f"Validation error while saving job for user {user.id}: {e}")
            raise JobCreationException(str(e))
        except Exception as e:
            logger.error(f"Error saving job for user {user.id}: {e}")
            raise JobCreationException(str(e))

    def update_status(self, user, job_data):
        """
        Updates the status of a job. Requires a valid User model to perform updating.

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
            raise JobNotFoundException(f"Job with {job_id} does not exist.")

    def update_status_by_id(self, job_id:str, job_status:str):
        """
        Updates the status of a job, does not require a valid User model to perform updating.

        Args:
            job_id (str): The job id to update.
            job_status (str): The name of the status to update.
            
        Returns:
            Job: The updated job object.

        Raises:
            ValidationError: If the job data is invalid.
            JobNotFoundException: If the job does not exist.
            InvalidJobStatus: If the job status is invalid.
        """
        data = {'job_id': job_id, 'job_status': job_status}

        serializer = UpdateJobStatusSerializer(data=data)
        # Raise an error if serializer is not valid
        if not serializer.is_valid():
            logger.error(f"UpdateJobStatusSerializer error: {serializer.errors}")
            raise ValidationError(serializer.errors)

        # Retrieve the validated job_id and job_status from the serializer
        job_id = serializer.validated_data.get('job_id')
        job_status = serializer.validated_data.get('job_status')

        try:
            # Retrieve the job and update its job_status
            job = Job.objects.get(job_id=job_id)
            job_status_instance = JobStatus.objects.get(name=job_status)
            job.job_status = job_status_instance
            job.save() 
            return job
        except Job.DoesNotExist:
            raise JobNotFoundException(f"Job with id {job_id} does not exist")
        except JobStatus.DoesNotExist:
            raise InvalidJobStatus(f"Invalid job status: {job_status}")
        except Exception as e:
            logger.error(f"Error updating job status for job_id {job_id}")
            raise JobUpdateException(str(e))
        
    def get_job_parameters(self, job_id):
        """
        Retrieves the parameters of a job by its job_id.

        Args:
            job_id (str): The job ID.

        Returns:
            dict: The job parameters.

        Raises:
            JobNotFoundException: If the job does not exist.
        """
        try:
            job = Job.objects.get(job_id = job_id)
            return job.parameters
        except Job.DoesNotExist:
            raise JobNotFoundException(f"Job with {job_id} does not exist.")
    
    def get_parent_job(self, job_id) -> Job:
        """
        Retrieves parent job by the job_id.

        Args:
            job_id (str): The job ID.

        Returns:
            job: The parent job.
            None if no parent job exists.
        Raises:
            JobNotFoundException: If the job does not exist.
        """
        try:
            job = Job.objects.get(job_id=job_id)
            parent_job = job.parent_job
            if parent_job is None:
                # Return empty dict if parent job does not exist
                return None
            return parent_job
        except Job.DoesNotExist:
            raise JobNotFoundException(f"Child job with {job_id} does not exist.")
    
    def update_all_parent_jobs_as_completed(self, job_id: str):
        """
        Recursively sets the status of all parent jobs to 'completed'.

        This function should be invoked by final step of consumers to set all parent jobs to 'completed' status.
        
        Args:
            job_id (str): The job ID to start the process.

        Raises:
            JobNotFoundException: If the job or any parent job does not exist.
            JobUpdateException: If there is an error updating the job status.
        """
        try:
            job = Job.objects.get(job_id=job_id)
        except Job.DoesNotExist:
            logger.error(f"Job with ID {job_id} does not exist.")
            raise JobNotFoundException(f"Job with ID {job_id} does not exist.")
        
        while job.parent_job_id:
            try:
                parent_job = job.parent_job
                if parent_job is None:
                    break  # Break if no parent job exists

                self.update_status_by_id(parent_job.job_id, ValidJobStatus.COMPLETED.value)
                logger.info(f"Parent job {parent_job.job_id} set to completed.")
                job = parent_job  # Move up to the next parent job
            except Job.DoesNotExist:
                logger.error(f"Parent job with ID {job.parent_job_id} does not exist.")
                raise JobNotFoundException(f"Parent job with ID {job.parent_job_id} does not exist.")
            except Exception as e:
                logger.error(f"Error updating parent job status for job ID {job.parent_job_id}: {e}")
                raise JobUpdateException(str(e))
        
    def get_child_jobs(self, job_id: str, limit=10) -> list:
        """
        Retrieves all descendant jobs for a given job_id in a hierarchical structure.
        Args:
            job_id (str): The ID of the starting (root) job.
            limit (int): The maximum number of child jobs to retrieve.
        Returns:
            list: A list of job IDs starting from the given job_id down the hierarchy.
        """
        jobs = []  # Initialize with the root job_id
        queue = [job_id]    # Queue to process each job and find its children

        try:
            # Process each job in the queue and retrieve its children
            # Stop when limit is reached or when queue is empty
            while queue and len(jobs) < limit:
                current_job_id = queue.pop(0)  # Get the next job to process
                parent = Job.objects.get(job_id=current_job_id)

                # Add the parent job's ID and type to the results list
                job_meta = (parent.job_id, parent.job_type)
                jobs.append(job_meta)

                # Retrieve the single child of the current job, if it exists
                child = Job.objects.filter(parent_job_id=current_job_id).first()
                if child:
                    queue.append(child.job_id)  # Add the child job_id to the queue

                # Stop if the limit is reached
                if len(jobs) >= limit:
                    break
            return jobs

        except Exception as e:
            logger.error(f"Error retrieving child jobs for job_id {job_id}: {str(e)}")
            raise JobRetrievalException(f"Error retrieving child jobs for job_id {job_id}: {str(e)}")
    
    def has_access_to_job(self, user, job_id) -> bool:
        """
        Checks if a job belongs to a user.

        Args:
            user: The authenticated user.
            job_id (str): The job ID.

        Returns:
            bool: True if the job belongs to the user, False otherwise.
        """
        try:
            # Attempt to retrieve the job with the given job_id and user
            return Job.objects.filter(job_id=job_id, user=user).exists()
        except Exception as e:
            logger.error(f"Error checking job ownership for user {user.id} and job_id {job_id}: {str(e)}")
            return False