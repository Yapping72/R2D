from rest_framework import serializers
from jobs.serializers.UserStorySerializer import UserStorySerializer

class UMLDiagramSerializer(serializers.Serializer):
    """
    UML Diagram Serializer validates and expects all UML diagrams to have features, sub_features, and job_parameters fields.
    """
    features = serializers.ListField(child=serializers.CharField())
    sub_features = serializers.ListField(child=serializers.CharField())
    job_parameters = serializers.DictField(child=serializers.DictField(child=serializers.DictField(child=UserStorySerializer())))
