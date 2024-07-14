from rest_framework import serializers
from jobs.models import Job
from jobs.services.JobExceptions import JobNotFoundException

class GetJobSerializer(serializers.ModelSerializer):
    """
    Serializer class for retrieving a job. 
    Expects a job_id (uuid) as input.
    """
    job_id = serializers.UUIDField()

    def validate_job_id(self, job_id):
        """
        Checks if the job_id provided is valid, by attempting to retrieve a job record, with the provided job_id.
        """
        try:
            Job.objects.get(job_id=job_id)
            return job_id
        except Job.DoesNotExist:
            raise JobNotFoundException(f"Invalid job id provided - {job_id}")

    class Meta:
        model = Job
        fields = ['job_id', 'user']