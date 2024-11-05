import os
from framework.factories.interfaces.BaseRepositoryFactory import BaseRepositoryFactory
from diagrams.services.DiagramExceptions import DiagramRepositoryInstantiationError
from diagrams.repository.ClassDiagramRepository import ClassDiagramRepository
from diagrams.repository.ERDiagramRepository import ERDiagramRepository
from diagrams.repository.SequenceDiagramRepository import SequenceDiagramRepository

import logging
from enum import Enum 

# R2D Logger module
logger = logging.getLogger('application_logging')

class FactoryList(Enum):
    """
    List of repositories supported by this factory
    > CLASS_DIAGRAM_REPOSITORY = "class_diagram_repository"
    > ER_DIAGRAM_REPOSITORY = "er_diagram_repository"
    > SEQUENCE_DIAGRAM_REPOSITORY = "sequence_diagram_repository"
    """
    CLASS_DIAGRAM_REPOSITORY = "class_diagram_repository"
    ER_DIAGRAM_REPOSITORY = "er_diagram_repository"
    SEQUENCE_DIAGRAM_REPOSITORY = "sequence_diagram_repository"
    
class DiagramRetrievalRepositoryFactory(BaseRepositoryFactory):
    @staticmethod
    def get_repository(factory_name:str):
        """
        Returns a repository instance based on the name provided
        @params: factory_name
        Raises DiagramRepositoryInstantiationError if factory model cannot be initialized.
        """
        try: 
            if factory_name == FactoryList.CLASS_DIAGRAM_REPOSITORY.value:
                return ClassDiagramRepository()
            elif factory_name == FactoryList.ER_DIAGRAM_REPOSITORY.value:
                return ERDiagramRepository()
            elif factory_name == FactoryList.SEQUENCE_DIAGRAM_REPOSITORY.value:
                return SequenceDiagramRepository()
            else:
                return None
        except DiagramRepositoryInstantiationError as e:
            logger.error("Failed to initialize repository within DiagramRetrievalRepositoryFactory")
            raise e
            
