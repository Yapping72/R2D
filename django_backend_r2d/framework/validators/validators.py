from abc import ABC, abstractmethod
from rest_framework import serializers
from django.core.validators import validate_email as django_validate_email
from django.core.exceptions import ValidationError as DjangoValidationError

class BaseValidator(ABC):
    def validate_int(self, value):
        """
        Validate an integer value.

        :param value: Integer value to be validated.
        :return: Validated integer value or raise ValidationError.
        """
        try:
            return int(value)
        except ValueError:
            raise serializers.ValidationError("Invalid integer value")

    def validate_float(self, value):
        """
        Validate a float value.

        :param value: Float value to be validated.
        :return: Validated float value or raise ValidationError.
        """
        try:
            return float(value)
        except ValueError:
            raise serializers.ValidationError("Invalid float value")

    def validate_age(self, age):
        """
        Validate a person's age.

        :param age: Age value to be validated.
        :return: Validated age or raise ValidationError.
        """
        if age < 0 or age > 120:  # Adjust the age range as needed
            raise serializers.ValidationError("Invalid age")

    def validate_email(self, email):
        """
        Validate an email address.

        :param email: Email address to be validated.
        :return: Validated email address or raise ValidationError.
        """
        try:
            django_validate_email(email)
            return email
        except DjangoValidationError:
            raise serializers.ValidationError("Invalid email address")
