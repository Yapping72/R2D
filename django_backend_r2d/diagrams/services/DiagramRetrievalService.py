from diagrams.interfaces.BaseDiagramRetrievalService import BaseDiagramRetrievalService
from framework.factories.DiagramRetrievalRepositoryFactory import DiagramRetrievalRepositoryFactory
from framework.factories.DiagramRetrievalRepositoryFactory import FactoryList
from diagrams.services.DiagramExceptions import ClassDiagramRetrievalError, ERDiagramRetrievalError, SequenceDiagramRetrievalError
from jobs.services.JobService import JobService
from authentication.services.AuthenticationExceptions import AuthorizationError

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
        self.job_service = JobService()
        
    def retrieve_all_diagrams(self, user, job_id:str) -> dict:
        """
        Retrieve all diagrams including child diagrams for the given job_id.
        
        args:
            job_id: str - The job_id to retrieve the diagrams for.
        returns:
            dict - The dictionary containing the diagrams for the given job_id.
        raises:
            ClassDiagramRetrievalError - If there is an error retrieving class diagrams.
            ERDiagramRetrievalError - If there is an error retrieving ER diagrams.
            SequenceDiagramRetrievalError - If there is an error retrieving sequence diagrams.
        """
        class_diagrams = {}
        er_diagrams = {}    
        sequence_diagrams = {}
        try: 
            # Check if user has the rights to access these diagrams
            if not self.job_service.has_access_to_job(user, job_id):
                logger.error(f"User does not have access to job_id {job_id}")
                raise AuthorizationError("User does not have access to this job.")
            
            # Extract all job_ids and job_types for the given job_id
            job_ids = self.job_service.get_child_jobs(job_id)
            
            for job_id, job_type in job_ids:
                if job_type == "class_diagram":
                    class_diagrams = self.class_diagram_repo.get_audited_jobs_by_id(job_id)
                elif job_type == "er_diagram":
                    er_diagrams = self.er_diagram_repo.get_audited_jobs_by_id(job_id)
                elif job_type == "sequence_diagram":
                    sequence_diagrams = self.sequence_diagram_repo.get_audited_jobs_by_id(job_id)
                else:
                    logger.warning(f"Job type '{job_type}' not found.")
                    
            diagrams = {
                "class_diagrams": class_diagrams,
                "er_diagrams": er_diagrams,
                "sequence_diagrams": sequence_diagrams
            }
            
            logger.debug(f"Retrieved diagrams for job_id {job_id}: {diagrams}")
            return diagrams
        except (ClassDiagramRetrievalError, ERDiagramRetrievalError, SequenceDiagramRetrievalError) as e:
            logger.error(f"Error retrieving diagrams for job_id {job_id}: {str(e)}")
            raise e
        except AuthorizationError as e:
            logger.error(f"{user} does not have access to {job_id}")
            raise e
        
    def retrieve_diagram(self, user, job_id:str, diagram_name: str) -> dict:
        """
        Retrieve one diagram for the given job_id and diagram_name.
        
        args:
            job_id: str - The job_id to retrieve the diagram for.
            diagram_name: str - The diagram_name to retrieve the diagram for.
        returns:
            dict - The dictionary containing the diagram for the given job_id and diagram_name.
        raises:
            ClassDiagramRetrievalError - If there is an error retrieving class diagrams.
            ERDiagramRetrievalError - If there is an error retrieving ER diagrams.
            SequenceDiagramRetrievalError - If there is an error retrieving sequence diagrams.
        """
        try:
            if not self.job_service.has_access_to_job(user, job_id):
                logger.error(f"User does not have access to job_id {job_id}")
                raise AuthorizationError("User does not have access to this job.")
            
            if diagram_name == "class_diagram":
                diagrams = {
                    "job_id": job_id,
                    "class_diagrams": self.class_diagram_repo.get_audited_jobs_by_id(job_id)
                }
                return diagrams
            elif diagram_name == "er_diagram":
                diagrams = {
                    "job_id": job_id,
                    "er_diagrams": self.er_diagram_repo.get_audited_jobs_by_id(job_id)
                }
                return diagrams
            elif diagram_name == "sequence_diagram":
                diagrams = {
                    "job_id": job_id,
                    "sequence_diagrams": self.sequence_diagram_repo.get_audited_jobs_by_id(job_id)
                }
                return diagrams
            else:
                logger.warning(f"Diagram type '{diagram_name}' not found.")
                return {}
        except (ClassDiagramRetrievalError, ERDiagramRetrievalError, SequenceDiagramRetrievalError) as e:
            logger.error(f"Error retrieving {diagram_name} for job_id {job_id}: {str(e)}")
            raise e
        except AuthorizationError as e:
            logger.error(f"{user} does not have access to {job_id}")
            raise e
    
