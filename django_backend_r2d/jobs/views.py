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
        Creates or updates an existing job for the authenticated user.
        Returns the created or updated job_id if the operation is successful.
        """
        user = request.user
        job_data = request.data["payload"]
        logger.debug(user, job_data)
        job = job_service.save_job(user, job_data)
        
        return SyncAPIReturnObject(
            data={'job_id': job.job_id},
            message="Job parameters saved successfully.",
            success=True,
            status_code=status.HTTP_200_OK
        )

class UpdateJobStatusView(APIView):
    permission_classes = [IsAuthenticated]
    
    @BaseView.handle_exceptions
    def post(self, request):
        """
        Updates a job for the authenticated user. The payload should contain the job_id and the new status.
        The job_metadata object should contain the job_id and the new status.
        """
        user = request.user
        job_metadata = request.data["payload"]
        logger.debug(user, job_metadata)
        job = job_service.update_status(user, job_metadata)
        
        return SyncAPIReturnObject(
            data={'job_id': job.job_id},
            message="Job updated successfully.",
            success=True,
            status_code=status.HTTP_200_OK
        )