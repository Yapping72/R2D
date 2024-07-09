from rest_framework import serializers
from jobs.models import Job, JobStatus
from model_manager.models import ModelName

class JobSerializer(serializers.ModelSerializer):
    """
    Serializer for both requests and responses for the Job model.
    
    """
    # Define a SlugRelatedField for the job_status field
    job_status = serializers.CharField(write_only=True)
    model_name = serializers.CharField(write_only=True)  

    class Meta:
        model = Job
        fields = ["job_id", "user", "job_status", "job_details", "tokens", "parameters", "job_type", "parent_job", "model_name"]
    
    def create(self, validated_data):
        model_name = validated_data.pop('model_name')
        job_status = validated_data.pop('job_status')
        validated_data['job_status'] = JobStatus.objects.get(name=job_status)
        validated_data['model'] = ModelName.objects.get(name=model_name)
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        model_name = validated_data.pop('model_name', None)
        job_status = validated_data.pop('job_status', None)
        if model_name:
            instance.model = ModelName.objects.get(name=model_name)
        if job_status:
            instance.job_status = JobStatus.objects.get(name=job_status)
        return super().update(instance, validated_data)
    
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['job_status'] = instance.job_status.name
        ret['model_name'] = instance.model.name
        return ret