from rest_framework import serializers
from jobs.models import Job
from jobs.services.JobExceptions import JobNotFoundException

class CreateDiagramSerializer(serializers.Serializer):
    """
    This serializer is used to validate the input for the create_diagram view.
    Expects a job_id (uuid) and a job_type (str) as input.
    """
    job_id = serializers.UUIDField()
    job_type = serializers.CharField()

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
        
    def validate_job_type(self, job_type):
        """
        Validates the job status. Raises an exception if the status is invalid.
        """
        valid_job_types = ['Class Diagram', 'Sequence Diagram', 'ER Diagram']
        if job_type not in valid_job_types:
            logger.error(f"Invalid diagram type provided - {job_type} - Valid types are {valid_job_types}")
            raise serializers.ValidationError(f"Invalid diagram type provided - {job_type}")
        return job_type

    