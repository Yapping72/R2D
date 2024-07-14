from rest_framework import serializers

class CreateSequenceDiagramSerializer(serializers.Serializer):
    """
    Primary serializer when creating Sequence diagrams.
    This serializer is used to create Sequence diagrams from the output of ClassDiagramService and ERDiagramService.
    """
    features = serializers.ListField(child=serializers.CharField())
    descriptions = serializers.ListField(child=serializers.CharField())
    classes = serializers.ListField(child=serializers.CharField())
    helper_classes = serializers.ListField(child=serializers.CharField())
    