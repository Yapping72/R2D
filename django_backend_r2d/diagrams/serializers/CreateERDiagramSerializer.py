from rest_framework import serializers
from jobs.serializers.UserStorySerializer import UserStorySerializer

class CreateERDiagramSerializer(serializers.Serializer):
    """
    Primary serializer when creating ER diagrams.
    This serializer is used to create ER diagrams from the output of ClassDiagramService.
    """
    features = serializers.ListField(child=serializers.CharField())
    descriptions = serializers.ListField(child=serializers.CharField())
    classes = serializers.ListField(child=serializers.CharField())