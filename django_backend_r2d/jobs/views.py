from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from jobs.services.JobService import JobService
from framework.responses.SyncAPIReturnObject import SyncAPIReturnObject
from framework.views.BaseView import BaseView
from jobs.services.JobExceptions import *
from jobs.services.JobHistoryService import JobHistoryService

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
        request_payload = request.data["payload"]
        logger.info("api/jobs/save/ invoked")
        logger.info(f"Payload: {request_payload}")
        job = job_service.save_job(user, request_payload)
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
        Updates a job for the authenticated user. 
        The payload should contain the job_id and the new status.
        """
        user = request.user
        request_payload = request.data["payload"]
        logger.debug(user, request_payload)
        job = job_service.update_status(user, request_payload)
        
        return SyncAPIReturnObject(
            data={'job_id': job.job_id},
            message="Job updated successfully.",
            success=True,
            status_code=status.HTTP_200_OK
        )

class GetOneJobView(APIView):
    permission_classes = [IsAuthenticated]
    
    @BaseView.handle_exceptions
    def post(self, request):
        """
        Get a job for the authenticated user. 
        The payload should contain the job_id.
        """
        user = request.user
        request_payload = request.data["payload"]
        logger.debug(f"GetOneJobView: {user} {request_payload}")
        job = job_service.get_job_for_user(user, request_payload)
        logger.debug(f"Job Retrieved: {job}")
        
        return SyncAPIReturnObject(
            data=job,
            message="Job retrieved successfully.",
            success=True,
            status_code=status.HTTP_200_OK
        )

class GetAllJobsView(APIView):
    permission_classes = [IsAuthenticated]
    
    @BaseView.handle_exceptions
    def post(self, request):
        """
        Get all jobs for the authenticated user.
        """
        user = request.user
        jobs = job_service.get_all_jobs_for_user(user)
        logger.debug(f"GetAllJobsView: {jobs}")
        return SyncAPIReturnObject(
            data={'jobs': jobs},
            message="Jobs retrieved successfully.",
            success=True,
            status_code=status.HTTP_200_OK
        )

class GetJobHistoryView(APIView):
    permission_classes = [IsAuthenticated]
    
    @BaseView.handle_exceptions
    def post(self, request):
        """
        Get job history for the authenticated user.
        """
        user = request.user
        logger.debug(f"GetJobHistory: {user}")
        job_history = JobHistoryService.get_job_history(user)
        
        return SyncAPIReturnObject(
            data={'job_history': job_history},
            message="Job history retrieved successfully.",
            success=True,
            status_code=status.HTTP_200_OK
        )
        
class GetCompletedJobsView(APIView):
    permission_classes = [IsAuthenticated]
    
    @BaseView.handle_exceptions
    def post(self, request):
        """
        Get completed jobs for the authenticated user.
        """
        user = request.user
        logger.debug(f"GetCompletedJobs: {user}")
        completed_jobs = job_service.get_all_completed_jobs_for_user(user)    
        return SyncAPIReturnObject(
            data={'completed_jobs': completed_jobs},
            message="Completed jobs for user successfully.",
            success=True,
            status_code=status.HTTP_200_OK
        )


class DeleteJobsView(APIView):
    permission_classes = [IsAuthenticated]

    @BaseView.handle_exceptions
    def delete(self, request):
        """
        Delete  jobs for the authenticated user. If a job_id is provided in the request data,
        it will delete that specific completed job; otherwise, it will delete all completed jobs for the user.
        """
        user = request.user
        job_id = request.data.get("job_id", None)

        if job_id:
            logger.debug(f"DeleteJobs: {user} {job_id}")
            job_service.delete_job(user, job_id)
            data = {'job_id': job_id}
            message = "Job deleted successfully."
        else:
            data = {}
            message = "No job_id provided."
                    
        return SyncAPIReturnObject(
            data=data,
            message=message,
            success=True,
            status_code=status.HTTP_200_OK
        )