from abc import ABC, abstractmethod

class BaseModel(ABC):
    """
    Defines the interface for a model that can be used within R2D.
    """
    @abstractmethod
    def analyze(self, prompt:str, response_schema:dict):
        """
        Analyze the prompt and context and return the generated output.
        args:
            prompt (str): The prompt to be analyzed.
            response_schema (dict): Optional schema for structured response.
        """
        pass
