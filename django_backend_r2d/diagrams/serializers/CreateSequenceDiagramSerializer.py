from rest_framework import serializers

class CreateSequenceDiagramSerializer(serializers.Serializer):
    """
    Primary serializer to use when creating sequence diagrams. 
    This serializer is expected to be used when creating sequence diagrams from class diagrams and er diagrams.
    """
    features = serializers.ListField(child=serializers.CharField())
    entities = serializers.ListField(child=serializers.CharField())
    entity_descriptions = serializers.ListField(child=serializers.CharField())
    # For flexibility, allow null values for the following fields
    classes = serializers.ListField(child=serializers.CharField(), required=False, allow_null=True)
    class_descriptions = serializers.ListField(child=serializers.CharField(), required=False, allow_null=True)
    helper_classes = serializers.ListField(child=serializers.CharField(), required=False, allow_null=True)
    