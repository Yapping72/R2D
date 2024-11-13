from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from framework.responses.SyncAPIReturnObject import SyncAPIReturnObject
from framework.views.BaseView import BaseView
from diagrams.services.DiagramRetrievalService import DiagramRetrievalService

# Initialize logging class and retrieve the custom user model
import logging
logger = logging.getLogger('application_logging')

from django.contrib.auth import get_user_model
User = get_user_model()

# Initialize the diagram retrieval service
diagram_retrieval_service = DiagramRetrievalService() 

class RetrieveAllDiagramsView(APIView):
    permission_classes = [IsAuthenticated]

    @BaseView.handle_exceptions
    def post(self, request):
        """
        Retrieves all diagrams for the authenticated user.
        The payload should contain a job_id.
        """
        user = request.user
        request_payload = request.data
        job_id = request_payload.get('job_id')
        logger.info("api/diagrams/retrieve-diagrams/ invoked")
        logger.debug(f"Payload: {request_payload}")
        
        diagrams = diagram_retrieval_service.retrieve_all_diagrams(user, job_id)
        
        return SyncAPIReturnObject(
            data={'job_id': job_id, "diagrams": diagrams},
            message= f"Retrieved diagrams for {job_id} successfully.",
            success=True,
            status_code=status.HTTP_200_OK
        )

class RetrieveOneDiagramView(APIView):
    permission_classes = [IsAuthenticated]

    @BaseView.handle_exceptions
    def post(self, request):
        """
        Retrieves a single diagram for the authenticated user.
        The payload should contain a job_id.
        """
        user = request.user
        request_payload = request.data
        job_id = request_payload.get('job_id')
        diagram_name = request_payload.get('diagram_name')
        
        logger.info("api/diagrams/retrieve-one-diagram/ invoked")
        logger.debug(f"Payload: {request_payload}")
        
        diagram = diagram_retrieval_service.retrieve_diagram(user, job_id, diagram_name)
        
        return SyncAPIReturnObject(
            data={'job_id': job_id, "diagram": diagram},
            message= f"Retrieved diagram for {job_id} successfully.",
            success=True,
            status_code=status.HTTP_200_OK
        )