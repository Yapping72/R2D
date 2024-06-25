from django.db import models, IntegrityError
from django.contrib.auth import get_user_model
User = get_user_model()
import uuid

class JobStatus(models.Model):
    """
    Table to store valid job statuses. 
    Used to normalize job status in Job model.
    id | name | code 
    1 | Draft | 1 
    2 | Queued | 2 
    3 | Submitted | 3 
    4 | Error Failed to Submit | 4
    5 | Processing | 5
    6 | Error Failed to Process | 6
    7 | Job Aborted | 7
    8 | Completed | 8
    """
    name = models.CharField(max_length=50, unique=True)
    code = models.PositiveSmallIntegerField(unique=True)
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Job Status"
        verbose_name_plural = "Job Statuses"
        ordering = ['code']

    def save(self, *args, **kwargs):
        # Prevent changes to predefined statuses
        if self.pk:
            raise IntegrityError("Modification of predefined job statuses is not allowed.")
        super().save(*args, **kwargs)
        
class Job(models.Model):
    """
    Job object that represents a user uploaded job
    job_id: UUID of the job
    user: User who uploaded the job
    job_status: Status of the job - Draft, Queued, Submission Error, Processing, Job Aborted, Completed, Processing Error
    job_details: Details of the job
    tokens: Number of tokens in parameters 
    parameters: Parameters that are sent to LLM for processing
    created_timestamp: Timestamp when the job was created
    last_updated_timestamp: Timestamp when the job was last updated
    """
    job_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job_status = models.ForeignKey(JobStatus, to_field='code', on_delete=models.PROTECT)
    job_details = models.TextField(max_length=100)
    tokens = models.IntegerField()
    parameters = models.JSONField()
    created_timestamp = models.DateTimeField(auto_now_add=True)
    last_updated_timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Job Id: {self.job_id}\nCreated By:{self.user}\nStatus:{self.job_status}\nCreated on:{self.created_timestamp}\nUpdated on:{self.last_updated_timestamp}"

