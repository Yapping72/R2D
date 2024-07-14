from rest_framework import serializers
from jobs.models import JobHistory

class JobHistorySerializer(serializers.ModelSerializer):
    job_id = serializers.UUIDField(source='job.job_id')
    previous_status = serializers.CharField(source='previous_status.name', allow_null=True)
    current_status = serializers.CharField(source='current_status.name')
    job_type = serializers.CharField()

    class Meta:
        model = JobHistory
        fields = ['job_id', 'previous_status', 'current_status', 'job_type', 'created_timestamp', 'last_updated_timestamp']
