from django.db import models, IntegrityError
from django.contrib.auth import get_user_model
User = get_user_model()
import uuid

class JobStatus(models.Model):
    """Table to store valid job statuses. 
    Used to normalize job status in Job model."""
    
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
    job_status = models.ForeignKey(JobStatus, on_delete=models.PROTECT)
    job_details = models.TextField(max_length=100)
    tokens = models.IntegerField()
    parameters = models.JSONField()
    created_timestamp = models.DateTimeField(auto_now_add=True)
    last_updated_timestamp = models.DateTimeField(auto_now=True)

class JobManager(models.Manager):
    """
    Manager for Job model.
    """
    def for_user(self, user):
        return self.filter(user=user)
