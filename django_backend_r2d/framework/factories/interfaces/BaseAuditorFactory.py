from abc import ABC, abstractmethod

class BaseAuditorFactory(ABC):
    @staticmethod
    @abstractmethod
    def get_auditor():
        """Returns the auditor class that the factory is responsible for creating."""
        raise NotImplementedError("Subclasses of BaseAuditorFactory must implement get_auditor().")

