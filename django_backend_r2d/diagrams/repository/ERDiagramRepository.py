from diagrams.models import ERDiagram
from diagrams.serializers.ERDiagramSerializer import ERDiagramSerializer  
from diagrams.services.DiagramExceptions import ERDiagramRetrievalError, ERDiagramSavingError
from rest_framework.exceptions import ValidationError

import logging 
# Initialize the logger
logger = logging.getLogger('application_logging')

class ERDiagramRepository:
    """
    Repository class for saving and retrieving ER diagrams.
    """
    def save_diagram(self, job_id:str, chain_response: dict) -> list[dict]:
        """
        Iterate through the chain_response and save the er diagrams.
        
        args:
            job_id: str - The job_id to save the er diagrams for.
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
                diagram = {
                    "job": job_id,
                    "model_name": chain_response[model].get("model_name"),
                    "feature": diagram["feature"],
                    "diagram": diagram["diagram"],
                    "description": diagram["description"],
                    "entities": diagram["entities"],
                    "is_audited": chain_response[model].get("is_audited")
                }
                try:
                    # Save the diagram 
                    saved_diagram = self.save(diagram)
                    saved_diagrams.append(saved_diagram)
                except ERDiagramSavingError as e:
                    # If one diagram fails to save, log the error and continue to the next diagram
                    logger.error(f"Error while saving ER diagram: {str(e)} - {diagram}. Attempting to save the next diagram.")
                    failed_to_save_count += 1
                    failed_to_save_diagrams.append(diagram)
                    continue 
        
        # Logging summary of results
        if failed_to_save_diagrams:
            logger.error(f"Failed to save {len(failed_to_save_diagrams)} ER diagrams.")
            logger.error(f"Failed diagrams: {failed_to_save_diagrams}")
            
        logger.debug(f"Diagrams saved: {saved_diagrams}.")
        return saved_diagrams
                    
    def save(self, data: dict) -> dict:
        """
        Save the class diagram data to the database.
        args:
           data: dict - The data to be saved.
        raises:
            ValidationError - If the data is not valid.
            ERDiagramSavingError - If any other error occurs during saving.
        """
        try:
            serializer = ERDiagramSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return serializer.data
            else:
                raise ValidationError(serializer.errors)
        except ValidationError as e:
            logger.error(f"Validation error while saving class diagram: {str(e)}")
            raise ERDiagramSavingError(f"An error occurred while validating the class diagram. {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error while saving class diagram: {str(e)}")
            raise ERDiagramSavingError("An unexpected error occurred while saving the class diagram.")
    
    def get_by_id(self, job_id:str) -> dict:
        """
        Get the er diagrams by job_id.
        args:
            job_id: str - The job_id to search for.
        returns:
            list - The class diagrams for the job_id. 
        """
        try:
            er_diagrams = ERDiagram.objects.filter(job_id=job_id).values()
            return list(er_diagrams)
        except Exception as e:
            logger.error(f"Error while retrieving class diagrams by job_id: {str(e)}")
            raise ERDiagramRetrievalError("An error occurred while retrieving the class diagrams.")
    