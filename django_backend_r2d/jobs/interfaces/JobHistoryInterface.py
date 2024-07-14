from abc import ABC, abstractmethod

class JobHistoryInterface(ABC):
    @abstractmethod
    def log_job_history(self, **kwargs):
        """Log the history of a job"""
        pass
