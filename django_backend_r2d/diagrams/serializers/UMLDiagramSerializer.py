from rest_framework import serializers
from jobs.serializers.UserStorySerializer import UserStorySerializer

class UMLDiagramSerializer(serializers.Serializer):
    """
    Serializer used to create UML diagrams from User Stories.
    This is the primary Serializer for ClassDiagram creation, it also serves as a fallback serializer for other diagrams
    
    args:
        features: list - The features of the UML diagram
        sub_features: list - The sub-features of the UML diagram
        job_parameters: dict - The job parameters comprises User Stories
    """
    features = serializers.ListField(child=serializers.CharField())
    sub_features = serializers.ListField(child=serializers.CharField())
    job_parameters = serializers.DictField(child=serializers.DictField(child=serializers.DictField(child=UserStorySerializer())))
