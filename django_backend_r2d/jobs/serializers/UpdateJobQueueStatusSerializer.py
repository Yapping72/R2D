from rest_framework import serializers
from jobs.models import JobQueue
from jobs.constants import ValidJobStatus

class UpdateJobQueueStatusSerializer(serializers.Serializer):
    """
    The serializer class for updating the job status.
    Expects a job_id (uuid) and a job_status (str) as input.
    raises: 
        ValidationError: if the job_id or job_status is invalid.
    """
    job_id = serializers.UUIDField()
    job_status = serializers.CharField()

    def validate_job_id(self, job_id:str):
        """
        Checks if the job_id provided is valid, by attempting to retrieve a job record, with the provided job_id.
        """
        try:
            JobQueue.objects.get(job_id=job_id)
            return job_id
        except Job.DoesNotExist:
            raise serializers.ValidationError("Invalid job id provided - {job_id}", code='invalid_job_id')      
          
    def validate_job_status(self, job_status:str):
        """
        Validates the job status.
        Args:
            job_status (str): The job status to validate. 
        
        Valid job status: Submitted, Processing, Error Failed to Process, Job Aborted, Completed
        """
        if job_status in [status.value for status in ValidJobStatus]:
            return job_status
        raise serializers.ValidationError(f"Invalid job status provided - {job_status}", code='invalid_job_status')

    