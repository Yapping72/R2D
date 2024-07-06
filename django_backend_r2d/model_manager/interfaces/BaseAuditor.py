from abc import ABC, abstractmethod
from model_manager.interfaces.BasePromptTemplate import BasePromptTemplate

class BaseAuditor(ABC):
    """
    Defines the interface for an auditor that can be used within R2D.
    Auditors are LLMs that audits the response from an earlier model.
    """
    def __init__(self, model_name:str=""):
        self.model_name = model_name
        
    @abstractmethod
    def audit(self, prompt: str, response_schema:dict, model_response:dict):
        """
        Audit the results of the model and return the audit results.
        args:
            prompt (str): The prompt to be audited.
            response_schema (dict): Optional schema for structured response.
            model_response (dict): The response from the model that needs to be audited.
        """
        pass
