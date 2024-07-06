from diagrams.interfaces.BaseDiagramSavingService import BaseDiagramSavingService
from diagrams.models import ClassDiagram
from diagrams.serializers.ClassDiagramSerializer import ClassDiagramSerializer  
from diagrams.services.DiagramExceptions import * 
from rest_framework.exceptions import ValidationError

import logging 
# Initialize the logger
logger = logging.getLogger('application_logging')

class ClassDiagramSavingService:
    def save(self, data: dict) -> dict:
        """
        Save the class diagram data to the database.
        args:
           data: dict - The data to be saved.
        raises:
            ValidationError - If the data is not valid.
            ClassDiagramSavingError - If any other error occurs during saving.
        """
        try:
            serializer = ClassDiagramSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return serializer.data
            else:
                raise ValidationError(serializer.errors)
        except ValidationError as e:
            logger.error(f"Validation error while saving class diagram: {str(e)}")
            raise ClassDiagramSavingError(f"An error occurred while validating the class diagram. {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error while saving class diagram: {str(e)}")
            raise ClassDiagramSavingError("An unexpected error occurred while saving the class diagram.")