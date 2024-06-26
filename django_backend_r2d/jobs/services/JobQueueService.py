import logging
from django.utils import timezone
from jobs.models import Job, JobQueue, JobStatus

logger = logging.getLogger('application_logging')

class JobQueueService(JobQueueInterface):
    def __init__(self, job_queue: JobQueue):
        self.job_queue = job_queue