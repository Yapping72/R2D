from rest_framework import serializers
from jobs.models import Job, JobStatus
from model_manager.models import ModelName

class JobSerializer(serializers.ModelSerializer):
    """
    Serializer for both requests and responses for the Job model.
    """
    # Define a SlugRelatedField for the job_status field
    job_status = serializers.SlugRelatedField(slug_field='name', queryset=JobStatus.objects.all())
    model = serializers.SlugRelatedField(slug_field='name', queryset=ModelName.objects.all())
    
    class Meta:
        model = Job
        fields = '__all__'

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['job_status'] = instance.job_status.name
        return ret
