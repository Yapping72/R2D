from abc import ABC, abstractmethod

class BaseAuditorFactory(ABC):
    @abstractmethod
    def get_auditor(self, auditor_name:str):
        """Returns the auditor class that the factory is responsible for creating."""
    raise NotImplementedError("Subclasses of BaseDaoFactory must implement get_dao().")

