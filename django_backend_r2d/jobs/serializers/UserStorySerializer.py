from rest_framework import serializers

class UserStorySerializer(serializers.Serializer):
    """
    User Story Serializer validates and expects all user stories to have id, requirement, services_to_use*, acceptance_criteria, and additional_information fields.
    id is a string that represents the unique identifier of the user story.
    requirement is a string that represents the requirement of the user story. "As a user... I want to.. So that.."
    services_to_use is a list of services that the user story will use. This field is optional.
    acceptance_criteria is a string that describes the acceptance criteria for the user story.
    additional_information is a string that contains any additional information about the user story. This field is optional.
    """
    id = serializers.CharField()
    requirement = serializers.CharField()
    services_to_use = serializers.ListField(
        child=serializers.CharField(allow_blank=True), # This allows empty strings
        allow_empty=True  # This allows empty lists
    )
    acceptance_criteria = serializers.CharField()
    additional_information = serializers.CharField(allow_blank=True)
