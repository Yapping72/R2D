from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status


from framework.responses.SyncAPIReturnObject import SyncAPIReturnObject
from framework.views.BaseView import BaseView

from jobs.services.JobService import JobService
from diagrams.services.ClassDiagramService import ClassDiagramService
from diagrams.repository.ClassDiagramRepository import ClassDiagramRepository
from model_manager.constants import ModelProvider, OpenAIModels

# Initialize logging class and retrieve the custom user model
import logging
logger = logging.getLogger('application_logging')
from django.contrib.auth import get_user_model
User = get_user_model()

class CreateClassDiagram(APIView):
    """
    API Endpoint for creating class diagrams.
    Payload: 
        job_id (uuid) - The job id to retrieve job parameters.
        diagram_type (str) - The type of diagram to create.
    """
    permission_classes = [IsAuthenticated]

    # Create the class responsible for creating class diagrams
    class_diagram_service = ClassDiagramService()
    
    # Create the class responsible for saving class diagrams
    class_diagram_repository = ClassDiagramRepository()
    
    @BaseView.handle_exceptions
    def post(self, request):
        """
        Expects a payload containing job_id to retrieve job parameters.
        Endpoint for creating or resubmitting a job.
        """
        pass 
