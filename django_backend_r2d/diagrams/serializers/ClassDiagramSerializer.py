from rest_framework import serializers
from diagrams.models import ClassDiagram
from model_manager.models import ModelName

class ClassDiagramSerializer(serializers.ModelSerializer):
    """
    Define the serializer for the ClassDiagram model.
    fields:
        job: str - The job of the class diagram.
        model_name: str - The name of the model.
        feature: list - The feature of the class diagram.
        diagram: str - The mermaid representation of the class diagram.
        description: str - The description of the class diagram.
        classes: list - The classes of the class diagram.
        helper_classes: list - The helper classes of the class diagram.
        is_audited: bool - Whether the class diagram has
    """
    model_name = serializers.CharField(write_only=True)  
    
    class Meta:
        model = ClassDiagram
        fields = ['job', 'model_name', 'feature', 'diagram', 'description', "helper_classes",'classes', 'is_audited', 'created_timestamp', 'last_updated_timestamp']

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