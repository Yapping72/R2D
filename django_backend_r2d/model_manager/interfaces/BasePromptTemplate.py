from abc import ABC, abstractmethod

class BasePromptTemplate(ABC):
    """
    Defines the interface for a prompt template that can be used within R2D.
    """
    @abstractmethod
    def get_prompt(self, job_parameters:dict, context:dict=None) -> str:
        """
        Generate a prompt based on the job parameters and embeddings context.
        job_parameters: dict - job_parameters stored in the jobs model.
        context: dict - additional context like embeddings retrieved the embeddings service or acceptance criteria (auditors).
        """
        pass 
        


