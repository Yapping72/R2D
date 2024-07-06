from abc import ABC, abstractmethod

class BaseDiagramService(ABC):
    """
    Interface that all diagram generating services must implement.
    """
    @abstractmethod
    def generate_diagram(self, job_parameters: dict, context: dict = None) -> dict:
        pass
