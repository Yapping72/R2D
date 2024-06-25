from rest_framework import serializers
from jobs.models import Job, JobStatus
from jobs.services.JobExceptions import InvalidJobStatus, JobNotFoundException

class UpdateJobStatusSerializer(serializers.Serializer):
    """
    The serializer class for updating the job status.
    Expects a job_id (uuid) and a job_status (str) as input.
    """
    job_id = serializers.UUIDField()
    job_status = serializers.CharField()

    def validate_job_id(self, job_id):
        """
        Checks if the job_id provided is valid, by attempting to retrieve a job record, with the provided job_id.
        """
        try:
            Job.objects.get(job_id=job_id)
            return job_id
        except Job.DoesNotExist:
            logger.error(f"Invalid job id provided - {job_id}")
            raise JobNotFoundException(f"Invalid job id provided - {job_id}")
        
    def validate_job_status(self, job_status):
        """
        Validates the job status. Raises an exception if the status is invalid.
        """
        try:
            JobStatus.objects.get(name=job_status)
            return job_status
        except JobStatus.DoesNotExist:
            logger.error(f"Invalid job status {job_status}")
            raise InvalidJobStatus(f"Invalid job status provided - {job_status}")

    