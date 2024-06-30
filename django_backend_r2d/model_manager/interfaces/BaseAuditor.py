from abc import ABC, abstractmethod
from model_manager.interfaces.BasePromptTemplate import BasePromptTemplate

class BaseAuditor(ABC):
    """
    Defines the interface for an auditor that can be used within R2D.
    Auditors are LLMs that audits the response from an earlier model.
    """
    @abstractmethod
    def audit(self, prompt: BasePromptTemplate, model_response:dict):
        """
        Audit the results of the model and return the audit results.
        The prompt should be a BasePromptTemplate object. 
        The BasePromptTemplate object will contain the prompt and any (optional) context that needs to be passed to the model.
        model_response will be the response from the model that needs to be audited.
        """
        pass
