from abc import ABC, abstractmethod

class BaseModelFactory(ABC):
    @staticmethod
    @abstractmethod
    def get_model():
        """Returns the model class that the factory is responsible for creating."""
        raise NotImplementedError("Subclasses of BaseModelFactory must implement get_model().")

