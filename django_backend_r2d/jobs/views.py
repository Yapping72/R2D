from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from jobs.services.JobService import JobService
from framework.responses.SyncAPIReturnObject import SyncAPIReturnObject
from framework.views.BaseView import BaseView
from jobs.services.JobExceptions import *

# Initialize logging class and retrieve the custom user model
import logging
logger = logging.getLogger('application_logging')
from django.contrib.auth import get_user_model
User = get_user_model()

job_service = JobService()
class JobSaveView(APIView):
    permission_classes = [IsAuthenticated]

    @BaseView.handle_exceptions
    def post(self, request):
        """
        Creates a new job for the authenticated user.
        """
        user = request.user
        job_data = request.data["payload"]
        logger.debug(user, job_data)
        job = job_service.save_job(user, job_data)
        
        return SyncAPIReturnObject(
            data={'job_id': job.job_id},
            message="Job created successfully.",
            success=True,
            status_code=status.HTTP_201_CREATED
        )
