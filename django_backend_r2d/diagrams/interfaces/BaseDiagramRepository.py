from abc import ABC, abstractmethod

class BaseDiagramRepository(ABC):
    """
    Interface that all diagram repository must implement.
    """
    @abstractmethod
    def save_diagram(self, job_id:str, chain_response: dict) -> list[dict]:
        """
        Iterate through the chain_response and save the er diagrams.
        
        args:
            job_id: str - The job_id to save the er diagrams for.
            chain_response: dict - The chain response to save.
        returns:
            saved_diagrams: list[dict] - List of diagrams (dict) objects that were saved.
        
        Assumes chain_response to be a dictionary containing one or more key-value pairs.
        e.g., {"model_1":"model_1_output", "model_2":"model_2_output"} this allows repository to be chain agnostic.
        """
    
    @abstractmethod
    def get_by_id(self, job_id:str, is_audited:bool) -> dict:
        """
        Get the diagrams by job_id.
        args:
            job_id: str - The job_id to search for.
            is_audited: bool - Denotes wheter the diagram retrieved should be the normal or audited version
        returns:
            list - The class diagrams for the job_id. 
        """
        
    
    