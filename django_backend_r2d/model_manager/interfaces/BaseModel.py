from abc import ABC, abstractmethod
from model_manager.interfaces.BasePromptTemplate import BasePromptTemplate

class BaseModel(ABC):
    """
    Defines the interface for a model that can be used within R2D.
    """
    @abstractmethod
    def analyze(self, prompt:BasePromptTemplate.get_prompt):
        """
        Analyze the prompt and context and return the generated output.
        Prompt accepts a BasePromptTemplate object. 
        The BasePromptTemplate object will contain the prompt and any (optional) context that needs to be passed to the model.
        """
        pass
