from diagrams.models import SequenceDiagram
from diagrams.serializers.SequenceDiagramSerializer import SequenceDiagramSerializer  
from diagrams.services.DiagramExceptions import SequenceDiagramSavingError
from rest_framework.exceptions import ValidationError
from diagrams.interfaces.BaseDiagramRepository import BaseDiagramRepository

import logging
# Initialize the logger
logger = logging.getLogger('application_logging')

class SequenceDiagramRepository(BaseDiagramRepository):
    """
    Repository class for saving and retrieving sequence diagrams.
    """
    def save_diagram(self, job_id:str, chain_response: dict) -> list[dict]:
        """
        Iterate through the chain_response and save the sequence diagrams.
        
        args:
            job_id: str - The job_id to save the sequence diagrams for.
            chain_response: dict - The chain response to save.
        returns:
            saved_diagrams: list[dict] - List of ERDiagram (dict) objects that were saved.
        
        Assumes chain_response to be a dictionary containing one or more key-value pairs.
        e.g., {"model_1":"model_1_output", "model_2":"model_2_output"} this allows repository to be chain agnostic.
        """
        saved_diagrams = []
        failed_to_save_count = 0 
        failed_to_save_diagrams = []
        
        for model in chain_response:
            # Process analysis_results diagrams
            for diagram in chain_response[model]["diagrams"]:
                # Add the job_id and model_name to the diagram
                logger.debug(f"Saving sequence diagram {diagram}.")

                diagram = {
                    "job": job_id,
                    "model_name": chain_response[model].get("model_name"),
                    "feature": diagram["feature"],
                    "diagram": diagram["diagram"],
                    "description": diagram["description"],
                    "actors": diagram["actors"],
                    "is_audited": chain_response[model].get("is_audited")
                }
                try:
                    # Save the diagram 
                    saved_diagram = self.save(diagram)
                    saved_diagrams.append(saved_diagram)
                except SequenceDiagramSavingError as e:
                    # If one diagram fails to save, log the error and continue to the next diagram
                    logger.error(f"Error while saving sequence diagram: {str(e)} - {diagram}. Attempting to save the next diagram.")
                    failed_to_save_count += 1
                    failed_to_save_diagrams.append(diagram)
                    continue 
                
    def save(self, data: dict) -> dict:
        """
        Save the sequence diagram data to the database.
        args:
           data: dict - The data to be saved.
        raises:
            ValidationError - If the data is not valid.
            SequenceDiagramSavingError - If any other error occurs during saving.
        """
        try:
            serializer = SequenceDiagramSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return serializer.data
            else:
                raise ValidationError(serializer.errors)
        except ValidationError as e:
            logger.error(f"Validation error while saving sequence diagram: {str(e)}", stack_info=True)
            raise SequenceDiagramSavingError(f"An error occurred while validating the class diagram. {str(e)}")
        except Exception as e:
            logger.error(f"Validation error while saving sequence diagram: {str(e)}", stack_info=True)
            raise SequenceDiagramSavingError("An unexpected error occurred while saving the class diagram.")
    