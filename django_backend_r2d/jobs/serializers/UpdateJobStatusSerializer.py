from rest_framework import serializers
from jobs.models import Job, JobStatus

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
            raise serializers.ValidationError("Invalid job id provided - {job_id}", code='invalid_job_id')      
          
    def validate_job_status(self, job_status):
        """
        Validates the job status. Raises an exception if the status is invalid.
        Not invoking a call to db to make the validation more efficient.
        Allowed values are: Draft, Queued, Submitted, Error Failed to Submit, Processing, Error Failed to Process, Job Aborted, Completed
        """
        if job_status in ['Draft', 'Queued', 'Submitted', 'Error Failed to Submit', 'Processing', 'Error Failed to Process', 'Job Aborted', 'Completed']:
            return job_status
        raise serializers.ValidationError(f"Invalid job status provided - {job_status}", code='invalid_job_status')

    