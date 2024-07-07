from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status


from framework.responses.SyncAPIReturnObject import SyncAPIReturnObject
from framework.views.BaseView import BaseView
from diagrams.services.ClassDiagramService import ClassDiagramService
from diagrams.services.ClassDiagramExceptions import *
from diagrams.services.ClassDiagramSavingService import ClassDiagramSavingService

# Initialize logging class and retrieve the custom user model
import logging
logger = logging.getLogger('application_logging')
from django.contrib.auth import get_user_model
User = get_user_model()


class_diagram_service = ClassDiagramService()

class CreateClassDiagram(APIView):
    permission_classes = [IsAuthenticated]

    @BaseView.handle_exceptions
    def post(self, request):
        """
        Expects a payload containing job_id to retrieve job parameters.
        Endpoint for creating or resubmitting a job.
        """
        user = request.user
        request_payload = request.data["payload"]

        return SyncAPIReturnObject(
            data={'class_diagram_id': class_diagram.class_diagram_id},
            message="Class diagram created successfully.",
            success=True,
            status_code=status.HTTP_200_OK
        )