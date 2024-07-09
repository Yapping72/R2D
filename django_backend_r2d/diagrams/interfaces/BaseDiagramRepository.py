from abc import ABC, abstractmethod

class BaseDiagramRepository(ABC):
    """
    Interface that all diagram saving services must implement.
    """
    @abstractmethod
    def save(self, data: dict) -> dict:
        """
        Save the diagram data to the database.
        :param data: dict - The data to be saved.
        :return: dict - The saved data.
        """
        pass
    
    @abstractmethod
    def get_diagrams_by_job_id(self, job_id: str) -> dict:
        """
        Retrieve all diagrams for a given job id.
        :param diagram_id: str - The id of the diagram to retrieve.
        :return: dict - The retrieved diagram.
        """
        pass
    
    def get_diagram_by_id(self, diagram_id: str) -> dict:
        """
        Retrieve a diagram by its id.
        :param diagram_id: str - The id of the diagram to retrieve.
        :return: dict - The retrieved diagram.
        """
        pass    
    
    
    
    