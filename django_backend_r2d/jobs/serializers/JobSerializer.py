from rest_framework import serializers
from jobs.models import Job

class JobSerializer(serializers.ModelSerializer):
    job_id = serializers.UUIDField(required=False)

    class Meta:
        model = Job
        fields = '__all__'