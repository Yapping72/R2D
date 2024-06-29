from abc import ABC, abstractmethod

class BaseModelFactory(ABC):
    @abstractmethod
    def get_model(self, model_name:str):
        """Returns the model class that the factory is responsible for creating."""
    raise NotImplementedError("Subclasses of BaseModelFactory must implement get_model().")

