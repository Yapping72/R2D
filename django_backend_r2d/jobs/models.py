from django.db import models, IntegrityError
from django.contrib.auth import get_user_model

User = get_user_model()
import uuid

from model_manager.models import ModelName

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
    attributes:
        job_id: UUID of the job
        user: User who uploaded the job
        job_status: Status of the job - Draft, Queued, Submission Error, Processing, Job Aborted, Completed, Processing Error
        job_details: Details of the job 
        tokens: Number of tokens in parameters 
        parameters: Parameters that are sent to LLM for processing
        created_timestamp: Timestamp when the job was created
        last_updated_timestamp: Timestamp when the job was last updated
        parent_job: link to the parent job if the job is a child job, else None
        job_type: Type of the job e.g., user_story, class_diagram, er_diagram, sequence_diagram, state_diagram
        model: ModelName object that the job is associated with
    """
    
    JOB_TYPES = (
        ('user_story', 'User Story'), 
        ('class_diagram', 'Class Diagram'), 
        ('er_diagram', 'ER Diagram'),
        ('sequence_diagram', 'Sequence Diagram'),
        ('state_diagram', 'State Diagram')
    )
    
    job_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job_status = models.ForeignKey(JobStatus, to_field='code', on_delete=models.PROTECT)
    job_details = models.TextField(max_length=100)
    tokens = models.IntegerField()
    parameters = models.JSONField()
    created_timestamp = models.DateTimeField(auto_now_add=True)
    last_updated_timestamp = models.DateTimeField(auto_now=True)
    job_type = models.CharField(max_length=50, choices=JOB_TYPES)
    parent_job = models.ForeignKey('self', on_delete=models.CASCADE, related_name='child_jobs', null=True, blank=True)
    model = models.ForeignKey(ModelName, on_delete=models.PROTECT)
    
    def __str__(self):
        return f"Job Id: {self.job_id}\nCreated By:{self.user}\nStatus:{self.job_status}\nCreated on:{self.created_timestamp}\nUpdated on:{self.last_updated_timestamp}"

    def save(self, *args, **kwargs):
        """
        Job save method to ensure that the job is considered a parent job if it has no parent job.
        """
        if not self.parent_job:
            self.parent_job = None  # Ensures that the job is considered a parent job
        super(Job, self).save(*args, **kwargs)
        
    def is_parent_job(self):
        """
        Check if the job is a parent job.
        return: True if the job is a parent job, False otherwise.
        """
        return self.parent_job is None
    
class JobQueue(models.Model):
    """
    JobQueue table will be referenced by Consumers e.g., LLM Service(s) to fetch jobs for processing.
    attributes:
        job: Job object that is in the queue
        status: Status of the job in the queue e.g., Queued, Processing, Completed, Failed
        job_type: Type of the job e.g., user_story, class_diagram, er_diagram, sequence_diagram, state_diagram
        consumer: Name of the consumer that is processing the job
        model_name: ModelName object that the job is associated with
        created_timestamp: Timestamp when the job was created
        last_updated_timestamp: Timestamp when the job was last updated
    """
    job = models.OneToOneField(Job, on_delete=models.CASCADE, primary_key=True)
    status = models.ForeignKey(JobStatus, to_field='code', on_delete=models.CASCADE)
    job_type = models.CharField(max_length=50)
    consumer = models.CharField(max_length=50, default="None") # Consumer name 
    model = models.ForeignKey(ModelName, on_delete=models.PROTECT)
    created_timestamp = models.DateTimeField(auto_now_add=True)
    last_updated_timestamp = models.DateTimeField(auto_now=True)
    
class JobHistory(models.Model):
    """
    JobHistory table will store the history of job status changes.
    
    attributes:
        job: Job object that is being updated
        user: User who updated the job
        previous_status: Previous status of the job
        current_status: Current status of the job
        job_type: Type of the job e.g., user_story, class_diagram, er_diagram, sequence_diagram, state_diagram
        created_timestamp: Timestamp when the history entry was created
        last_updated_timestamp: Timestamp when the history entry was last
    """
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    previous_status = models.ForeignKey(JobStatus, related_name='previous_status_histories', to_field='code', on_delete=models.CASCADE, null=True, blank=True)
    current_status = models.ForeignKey(JobStatus, related_name='current_status_histories', to_field='code', on_delete=models.CASCADE) 
    job_type = models.CharField(max_length=50)
    created_timestamp = models.DateTimeField(auto_now_add=True)
    last_updated_timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Job Id: {self.job.job_id}, Status: {self.status}, Updated on: {self.updated_timestamp}"
