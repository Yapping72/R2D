class JobCreationException(Exception):
    def __init__(self, message="Unspecified error occurred while creating job."):
        self.error_message = f"JobCreationException: {message}"
        super().__init__(self.error_message)

class JobUpdateException(Exception):
    def __init__(self, message="Unspecified error occurred while updating job."):
        self.error_message = f"JobUpdateException: {message}"
        super().__init__(self.error_message)

class JobDeleteException(Exception):
    def __init__(self, message="Unspecified error occurred while deleting job."):
        self.error_message = f"JobDeleteException: {message}"
        super().__init__(self.error_message)

class InvalidJobStatus(Exception):
    def __init__(self, message="Invalid job status provided."):
        self.error_message = f"InvalidJobStatus: {message}"
        super().__init__(self.error_message)
        
class JobNotFoundException(Exception):
    def __init__(self, message="Job not found."):
        self.error_message = f"JobNotFoundException: {message}"
        super().__init__(self.error_message)