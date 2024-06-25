from rest_framework import serializers
from jobs.models import Job, JobStatus

class JobSerializer(serializers.ModelSerializer):
    # Define a SlugRelatedField for the job_status field
    job_status = serializers.SlugRelatedField(slug_field='name', queryset=JobStatus.objects.all())

    class Meta:
        model = Job
        fields = '__all__'

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['job_status'] = instance.job_status.name
        return ret
