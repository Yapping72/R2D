from abc import ABC, abstractmethod

class JobServiceInterface(ABC):
    """Interface for job services to implement - mandates the implementation of save_job, update_status, delete and get job methods"""
    @abstractmethod
    def save_job(self, **kwargs):
        """Create or Update an existing job"""
        pass

    @abstractmethod
    def update_status(self, **kwargs):
        """Update the job status of an existing job"""
        pass
    
    @abstractmethod
    def get_job_for_user(self, job_id, user):
        """Get a job for a user"""
        pass
    
    def get_all_jobs_for_user(self, user):
        """Get all jobs for a user"""
        pass    