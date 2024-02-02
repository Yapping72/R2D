from rest_framework import serializers
from abc import ABC, abstractmethod
from django.db import models
from framework.validators.validators import BaseValidator  

class BaseSerializer(serializers.Serializer, ABC):
    def __init__(self):
        self.base_validator = BaseValidator()

    @abstractmethod
    def create_model(self) -> models:
        """
        Get the validated data in a format needed by the DAO.

        :return: valid model object.
        """
        raise NotImplementedError

    @abstractmethod
    def is_valid(self) -> bool:
        """
        Check if the serializer is valid.

        :param raise_exception: Whether to raise a ValidationError if validation fails.
        :return: True if valid, False otherwise.
        """
        raise NotImplementedError
