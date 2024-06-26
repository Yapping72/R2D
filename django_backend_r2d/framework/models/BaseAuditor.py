from abc import ABC, abstractmethod

class BaseAuditor(ABC):    
    """
    Defines the interface for all auditors. 
    Auditors are used to audit the results that are returned by LLMs.
    """
    @abstractmethod
    def audit(self):
        """
        Audits the results that are returned by LLMs.
        
        Parameters:
        result (dict): The result data returned by the LLM to be audited.
        
        Returns:
        bool: True if the audit passes, False otherwise.
        """
        raise NotImplementedError("Subclasses of BaseResponse must implement transform().")
