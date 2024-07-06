from abc import ABC, abstractmethod

class BaseModel(ABC):    
    """
    Defines the interface for all LLMs. 
    LLMs are used to perform domain logic.
    """
    @abstractmethod
    def analyze(self):
        """
        Submits the request to the LLM.
        
        Parameters:
        input_data (dict): The input data to be analyzed by the LLM.
        
        Returns:
        dict: The result of the analysis performed by the LLM.
        """
        raise NotImplementedError("Subclasses of BaseResponse must implement transform().")
    