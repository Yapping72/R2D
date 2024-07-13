from rest_framework import serializers
from jobs.models import JobQueue, JobStatus
from jobs.constants import ValidJobStatus

class UpdateJobQueueStatusSerializer(serializers.Serializer):
    """
    The serializer class for updating the job status.
    args:
        job_id (str): The job id to update.
        job_status (str): The job status to update.
        consumer (str): The consumer to process the job. (Optional) "None" by default
    raises: 
        ValidationError: if the job_id or job_status is invalid.
    """
    job_id = serializers.UUIDField()
    job_status = serializers.CharField()
    consumer = serializers.CharField(required=False)
    
    def validate_job_id(self, job_id:str):
        """
        Checks if the job_id provided is valid, by attempting to retrieve a job record, with the provided job_id.
        """
        try:
            JobQueue.objects.get(job_id=job_id)
            return job_id
        except Job.DoesNotExist:
            raise serializers.ValidationError(f"Invalid job id provided - {job_id}", code='invalid_job_id')      
          
    def validate_job_status(self, job_status:str):
        """
        Validates the job status.
        Args:
            job_status (str): The job status to validate. 
        
        Valid job status: Submitted, Processing, Error Failed to Process, Job Aborted, Completed
        """
        if job_status in [status.value for status in ValidJobStatus]:
            return JobStatus.objects.get(name=job_status)
        raise serializers.ValidationError(f"Invalid job status provided - {job_status}", code='invalid_job_status')

    def validate_consumer(self, consumer: str):
        """
        Validates the consumer.
        Args:
            consumer (str): The consumer to process the job.
        """
        valid_consumers = ["UserStoryConsumer", "ClassDiagramConsumer", "ERDiagramConsumer", "SequenceDiagramConsumer", "StateDiagramConsumer"]
        
        if consumer in valid_consumers or consumer == 'None':
            return consumer
        
        raise serializers.ValidationError(f"Invalid consumer provided - {consumer}", code='invalid_consumer')

    def update(self, instance, validated_data):
        """
        Update method to apply validated data to the instance.
        """
        instance.job_status = validated_data.get('job_status', instance.job_status)
        instance.consumer = validated_data.get('consumer', instance.consumer)
        instance.save()
        return instance
