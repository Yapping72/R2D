from rest_framework import serializers
from diagrams.models import ERDiagram
from model_manager.models import ModelName

class ERDiagramSerializer(serializers.ModelSerializer):
    """
    Define the serializer for the ERDiagram model.
    fields:
        job: str - The job of the ER diagram.
        model_name: str - The name of the model.
        feature: list - The feature of the ER diagram.
        diagram: str - The mermaid representation of the ER diagram.
        description: str - The description of the ER diagram.
        entities: list - The entities of the er diagram.
        is_audited: bool - Whether the er diagram has been audited
    """
    model_name = serializers.CharField(write_only=True)  
    
    class Meta:
        model = ERDiagram
        fields = ['job', 'model_name', 'feature', 'diagram', 'description', 'entities', 'is_audited', 'created_timestamp', 'last_updated_timestamp']

    def create(self, validated_data):
        model_name = validated_data.pop('model_name')
        validated_data['model'] = ModelName.objects.get(name=model_name)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        model_name = validated_data.pop('model_name', None)
        if model_name:
            model_name = ModelName.objects.get(name=model_name)
            instance.model = model_name  # Use correct field name
        return super().update(instance, validated_data)

    def validate_model_name(self, value):
        try:
            model_name_instance = ModelName.objects.get(name=value)
        except ModelName.DoesNotExist:
            raise serializers.ValidationError("Model name is invalid.")
        return model_name_instance