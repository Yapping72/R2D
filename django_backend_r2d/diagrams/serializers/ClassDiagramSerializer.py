from rest_framework import serializers
from diagrams.models import ClassDiagram
from model_manager.models import ModelName

class ClassDiagramSerializer(serializers.ModelSerializer):
    """
    Define the serializer for the ClassDiagram model.
    fields:
        job: str - The job of the class diagram.
        model_name_str: str - The name of the model.
        feature: str - The feature of the class diagram.
        diagram: str - The mermaid representation of the class diagram.
        description: str - The description of the class diagram.
        classes: str - The classes of the class diagram.
        is_audited: bool - Whether the class diagram has
    """
    model_name_str = serializers.CharField(write_only=True)  

    class Meta:
        model = ClassDiagram
        fields = ['job', 'model_name_str', 'feature', 'diagram', 'description', 'classes', 'is_audited', 'created_timestamp', 'last_updated_timestamp']

    def create(self, validated_data):
        model_name_str = validated_data.pop('model_name_str')
        model_name = ModelName.objects.get(name=model_name_str)
        validated_data['model_name'] = model_name  # Use correct field name
        return super().create(validated_data)

    def update(self, instance, validated_data):
        model_name_str = validated_data.pop('model_name_str', None)
        if model_name_str:
            model_name = ModelName.objects.get(name=model_name_str)
            instance.model_name = model_name  # Use correct field name
        return super().update(instance, validated_data)

    def validate_model_name_str(self, value):
        if not ModelName.objects.filter(name=value).exists():
            raise serializers.ValidationError("Model name is invalid.")
        return value