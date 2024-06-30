from abc import ABC, abstractmethod

class BaseModelService(ABC):
    """
    Defines the interface for a model service that can be used within R2D.
    """
    @abstractmethod
    def start_chain(self, model_name:str, auditor_name:str, prompt:str):
        """
        Start the model chain with the model name and prompt.
        """
        pass

