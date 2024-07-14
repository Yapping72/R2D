import logging
from jobs.models import JobHistory
from jobs.interfaces.JobHistoryInterface import JobHistoryInterface
from jobs.serializers.JobHistorySerializer import JobHistorySerializer
logger = logging.getLogger('application_logging')

class JobHistoryService(JobHistoryInterface):
    @staticmethod
    def get_job_history(user):
        """
        Retrieve and serialize the job history for a given user.

        This method fetches the job history entries for the specified user, orders them
        by the creation timestamp in descending order, and serializes the data using
        the JobHistorySerializer.

        Args:
            user (User): The user whose job history is to be retrieved.

        Returns:
            list: A list of serialized job history entries, or an empty list if no
            job history is found or an error occurs.
        """
        
        try:
            job_history = JobHistory.objects.filter(user=user).order_by('-created_timestamp')
            if not job_history.exists():
                logger.debug(f"No job history found for user {user}")
                return []
            logger.debug(f"Retrieved {job_history.count()} job history entries for user {user}")
            # Serialize the job history data
            return JobHistorySerializer(job_history, many=True).data
        except Exception as e:
            logger.error(f"Failed to get job history for user {user}: {str(e)}")
            raise RetrieveJobHistoryException(f"Failed to retrieve job history: {str(e)}")
        
    @staticmethod
    def log_job_history(job, user, previous_status, current_status):
        """
        Create a new job history entry for the specified job.
        """
        try:
            JobHistory.objects.create(
                job=job,
                user=user,
                previous_status=previous_status,
                current_status=current_status,
                job_type=job.job_type
            )
            logger.debug(f"Job history logged for Job ID {job.job_id} from {previous_status} to {current_status}")
        except Exception as e:
            logger.error(f"Failed to log job history for Job ID {job.job_id}: {str(e)}")
            # Do not raise exception so that the job is not affected by history logging failure