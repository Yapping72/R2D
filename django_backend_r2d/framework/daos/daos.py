from abc import ABC, abstractmethod
from django.db import models

class BaseDao(ABC):
    model = None  # Inheriting classes must specify the model

    def get_one(self, id):
        """
        Retrieve a single record by its primary key (id).

        :param id: The primary key of the record to retrieve.
        :return: The retrieved record or None if not found.
        """
        try:
            return self.model.objects.get(pk=id)
        except self.model.DoesNotExist:
            return None

    def get_all(self):
        """
        Retrieve all records for the model.

        :return: A queryset containing all records.
        """
        return self.model.objects.all()

    def create(self, **kwargs):
        """
        Create a new record with the provided data.

        :param kwargs: Keyword arguments containing field values for the new record.
        :return: The created record.
        """
        return self.model.objects.create(**kwargs)

    def update(self, id, **kwargs):
        """
        Update an existing record identified by its primary key (id).

        :param id: The primary key of the record to update.
        :param kwargs: Keyword arguments containing field values to update.
        :return: The updated record or None if not found.
        """
        try:
            instance = self.model.objects.get(pk=id)
            for key, value in kwargs.items():
                setattr(instance, key, value)
            instance.save()
            return instance
        except self.model.DoesNotExist:
            return None

    def delete(self, id):
        """
        Delete an existing record identified by its primary key (id).

        :param id: The primary key of the record to delete.
        :return: True if the record was deleted, False if not found.
        """
        try:
            instance = self.model.objects.get(pk=id)
            instance.delete()
            return True
        except self.model.DoesNotExist:
            return False
