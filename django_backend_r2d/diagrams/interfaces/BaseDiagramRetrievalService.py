from abc import ABC, abstractmethod

class BaseDiagramRetrievalService(ABC):
    """
    Interface that all diagram retrieval services must implement.
    This service will be responsible for extracting and parsing diagrams for frontend consumption.
    """
    @abstractmethod
    def retrieve_all_diagrams(self, job_id:str) -> dict:
        """
        Retrieve the diagrams for the given job_id.
        
        args:
            job_id: str - The job_id to retrieve the diagrams for.
        returns:
            dict - The dictionary containing the diagrams for the given job_id.
        """
    
    @abstractmethod
    def retrieve_diagram(self, job_id:str, diagram_name) -> dict:
        """
        Retrieve the diagram for the given job_id and diagram_name.
        
        args:
            job_id: str - The job_id to retrieve the diagram for.
            diagram_name: str - The diagram_name to retrieve the diagram for.
        returns:
            dict - The dictionary containing the diagram for the given job_id and diagram_name.
        """
    