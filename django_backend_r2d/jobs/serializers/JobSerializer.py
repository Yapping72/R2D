from rest_framework import serializers
from jobs.models import Job, JobStatus
from model_manager.models import ModelName
import json
import re

class JobSerializer(serializers.ModelSerializer):
    """
    Serializer when creating or working with Job model instances.
    Expects:
        job_id: The job id
        user: The user who created the job
        job_status: The status of the job
        job_details: Details of the job
        tokens: Number of tokens in parameters (Optional)
        parameters: Parameters that are sent to LLM for processing
        job_type: Type of the job e.g., user_story, class_diagram, er_diagram, sequence_diagram, state_diagram
        parent_job: link to the parent job if the job is a child job, else None
        model: ModelName object that the job is associated with
    
    Computes:
        job_status: The status of the job
        model_name: The name of the model associated with the
        tokens: Number of tokens in parameters, if key is not present, will calculate the number of tokens present in parameters.
    """
    # Define a SlugRelatedField for the job_status field
    job_status = serializers.CharField(write_only=True)
    model_name = serializers.CharField(write_only=True)  

    class Meta:
        model = Job
        fields = ["job_id", "user", "job_status", "job_details", "tokens", "parameters", "job_type", "parent_job", "model_name"]
        extra_kwargs = {
            'tokens': {'required': False, 'allow_null': True},
        }
             
    def create(self, validated_data):
        # Retrieve the model_name and job_status from the validated data
        # If tokens are not present, compute the number of tokens in the parameters
        
        model_name = validated_data.pop('model_name')
        job_status = validated_data.pop('job_status')
       
        validated_data['job_status'] = JobStatus.objects.get(name=job_status)
        validated_data['model'] = ModelName.objects.get(name=model_name)
        
        if 'tokens' not in validated_data or validated_data['tokens'] is None:
            parameters = validated_data.get('parameters', {})
            validated_data['tokens'] = self.compute_tokens(parameters)
        
        return super().create(validated_data)
    
    def compute_tokens(self, parameters):
        """
        Compute the number of tokens in the parameters, including nested JSON structures.
        """
        # Convert the JSON to a string
        json_string = json.dumps(parameters)
        
        # Count the words in the string
        token_count = len(re.findall(r'\w+', json_string))
        
        return token_count 
    def update(self, instance, validated_data):
        # Retrieve the model_name and job_status from the validated data
        # If tokens are not present, compute the number of tokens in the parameters
        model_name = validated_data.pop('model_name', None)
        job_status = validated_data.pop('job_status', None)
        
        if model_name:
            instance.model = ModelName.objects.get(name=model_name)
        if job_status:
            instance.job_status = JobStatus.objects.get(name=job_status)
            
        if 'tokens' not in validated_data or validated_data['tokens'] is None:
            parameters = validated_data.get('parameters', instance.parameters)
            validated_data['tokens'] = self.compute_tokens(parameters)
            
        return super().update(instance, validated_data)
    
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['job_status'] = instance.job_status.name
        ret['model_name'] = instance.model.name
        ret['last_updated_timestamp'] = instance.last_updated_timestamp
        # Ensure parameters is returned as an object, not a string
        if isinstance(ret['parameters'], str):
            try:
                ret['parameters'] = json.loads(ret['parameters'])
            except json.JSONDecodeError:
                # Handle cases where parameters might be an invalid JSON string
                ret['parameters'] = {}
        return ret
