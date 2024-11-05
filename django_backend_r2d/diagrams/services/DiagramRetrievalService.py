from diagrams.interfaces.BaseDiagramRetrievalService import BaseDiagramRetrievalService
from framework.factories.DiagramRetrievalRepositoryFactory import DiagramRetrievalRepositoryFactory
from framework.factories.DiagramRetrievalRepositoryFactory import FactoryList
from diagrams.services.DiagramExceptions import ClassDiagramRetrievalError, ERDiagramRetrievalError, SequenceDiagramRetrievalError


import logging 
# Initialize the logger
logger = logging.getLogger('application_logging')

class DiagramRetrievalService(BaseDiagramRetrievalService):
    def __init__(self):
        # diagrams will store all the diagrams for the given job_id
        """
        diagrams = {
            "job_id": 123456,
            "class_diagrams": [
                {
                    "feature": "feature1",
                    "diagram": "x-->a",
                    "classes": ["abc"],
                    "helper_classes": ["def"],
                    "description": ""
                },
                {
                    "feature": "feature2",
                    "diagram": "x-->a",
                    "classes": ["abc"],
                    "helper_classes": ["def"],
                    "description": ""
                }
            ],
            "er_diagrams": [
                {
                    "feature": "feature1",
                    "diagram": "x-->a",
                    "entities": ["abc"],
                    "description": ""
                }
            ],
            "sequence_diagrams": [
                {
                    "feature": "feature1",
                    "diagram": "x-->a",
                    "actors": ["abc"],
                    "description": ""
                }
            ]
        }
        """
        diagrams = {}
        # Initialize repositories for each diagram type
        # To onboard new repositories and diagram types, update the repository factory
        self.class_diagram_repo = DiagramRetrievalRepositoryFactory.get_repository(FactoryList.CLASS_DIAGRAM_REPOSITORY.value)
        self.er_diagram_repo = DiagramRetrievalRepositoryFactory.get_repository(FactoryList.ER_DIAGRAM_REPOSITORY.value)
        self.sequence_diagram_repo = DiagramRetrievalRepositoryFactory.get_repository(FactoryList.SEQUENCE_DIAGRAM_REPOSITORY.value)
        
    def retrieve_all_diagrams(self, job_id:str) -> dict:
        """
        Retrieve all diagrams including child diagrams for the given job_id.
        
        args:
            job_id: str - The job_id to retrieve the diagrams for.
        returns:
            dict - The dictionary containing the diagrams for the given job_id.
        """
        try: 
            class_diagrams = self.class_diagram_repo.get_by_id(job_id)
            sequence_diagrams = self.sequence_diagram_repo.get_by_id(job_id)
            er_diagrams = self.er_diagram_repo.get_by_id(job_id)
            
            diagrams = {
                "job_id": job_id,
                "class_diagrams": class_diagrams,
                "er_diagrams": er_diagrams,
                "sequence_diagrams": sequence_diagrams
            }
            
            logger.debug(f"Retrieved diagrams for job_id {job_id}: {diagrams}")
            return diagrams
        except (ClassDiagramRetrievalError, ERDiagramRetrievalError, SequenceDiagramRetrievalError) as e:
            logger.error(f"Error retrieving diagrams for job_id {job_id}: {str(e)}")
            raise e
        
    def retrieve_diagram(self, job_id:str, diagram_name: str) -> dict:
        """
        Retrieve one diagram for the given job_id and diagram_name.
        
        args:
            job_id: str - The job_id to retrieve the diagram for.
            diagram_name: str - The diagram_name to retrieve the diagram for.
        returns:
            dict - The dictionary containing the diagram for the given job_id and diagram_name.
        """
        try:
            if diagram_name == "class_diagram":
                diagrams = {
                    "job_id": job_id,
                    "class_diagrams": self.class_diagram_repo.get_by_id(job_id)
                }
                return diagrams
            elif diagram_name == "er_diagram":
                diagrams = {
                    "job_id": job_id,
                    "er_diagrams": self.er_diagram_repo.get_by_id(job_id)
                }
                return diagrams
            elif diagram_name == "sequence_diagram":
                diagrams = {
                    "job_id": job_id,
                    "sequence_diagrams": self.sequence_diagram_repo.get_by_id(job_id)
                }
                return diagrams
            else:
                logger.warning(f"Diagram type '{diagram_name}' not found.")
                return {}
        except (ClassDiagramRetrievalError, ERDiagramRetrievalError, SequenceDiagramRetrievalError) as e:
            logger.error(f"Error retrieving {diagram_name} for job_id {job_id}: {str(e)}")
            raise e
    
    def merge_diagrams(self, job_id:str, diagrams:dict, diagram_name:str) -> dict:
        """
        Merge the diagrams for the given job_id.
        
        args:
            job_id: str - The job_id to merge the diagrams for.
            diagrams: dict - The dictionary containing the diagrams for the given job_id.
        returns:
            dict - The dictionary containing the merged diagrams for the given job_id and diagram_name.
        """
        pass
    
