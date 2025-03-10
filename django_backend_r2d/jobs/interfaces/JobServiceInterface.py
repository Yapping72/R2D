from abc import ABC, abstractmethod

class JobServiceInterface(ABC):
    """
    Interface for job services to implement
    Methods to create, update and retrieve jobs
    """
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
    
    @abstractmethod
    def get_all_jobs_for_user(self, user):
        """Get all jobs for a user"""
        pass    
    
    @abstractmethod
    def get_job_by_id(self, job_id):
        """Get a job by its ID"""
        pass    
    
    @abstractmethod
    def update_status_by_id(self, job_id, job_status):
        """Update the status of a job by its ID"""
        pass

    def get_parent_job(self, job_id):
        """Get the parent job"""
        pass
    
    def get_job_parameters(self, job_id):
        """Get the job parameters"""
        pass    
    
    def update_all_parent_jobs_as_completed(self, job_id):
        """Update all parent jobs as completed"""
        pass
    
    @abstractmethod
    def update_job_description(self, job_id, description):
        """Update the job description"""
        pass