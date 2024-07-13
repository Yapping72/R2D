from enum import Enum 
from model_manager.constants import ModelProvider # Contains the ModelProvider and OpenAIModels enums
from model_manager.chains.AnalyzeAndAuditChainPromptBuilder import AnalyzeAndAuditChainPromptBuilder
from diagrams.chain_inputs.ClassDiagramAuditAnalyzeChainInputs import ClassDiagramAuditAnalyzeChainInputs
from diagrams.interfaces.BaseDiagramService import BaseDiagramService
from diagrams.serializers.UMLDiagramSerializer import UMLDiagramSerializer
from jobs.services.JobService import JobService
from jobs.services.JobExceptions import JobNotFoundException

import logging 
# Initialize the logger
logger = logging.getLogger('application_logging')

class ClassDiagramService(BaseDiagramService):
    """
    Service class for generating class diagrams and auditing them.
    Provides a concrete implementation of the BaseDiagramService class.
    Retrieves the job parameters, analysis context and audit criteria for the class diagram chain.
    Initializes the chain_input and prompt_builder to use for the analyze and audit chain.
    args: 
        model_provider (Enum): The model provider to use.
        model_name (Enum): The model name to use.
        auditor_name (Enum): The auditor name to use.
        job_id (str): The job ID to use.
    """
    def __init__(self, model_provider:ModelProvider, model_name: Enum, auditor_name:Enum, job_id:str):
        # Retrieve the job parameters, analysis context and audit criteria
        job_parameters = self.retrieve_job_parameters(job_id)
        analysis_context = self.retrieve_analysis_context(job_id)
        audit_criteria = self.retrieve_audit_criteria(job_id)

        # Initialize the chain input, prompt builder and serializer class
        chain_input = ClassDiagramAuditAnalyzeChainInputs(job_id=job_id, job_parameters=job_parameters, analysis_context=analysis_context, audit_criteria=audit_criteria)
        prompt_builder = AnalyzeAndAuditChainPromptBuilder() # Prompt builder for the Analyze and Audit chain
        serializer_class = UMLDiagramSerializer # Pass the serializer class to use
    
        super().__init__(model_provider, model_name, auditor_name, chain_input, prompt_builder, serializer_class)
    
    def retrieve_job_parameters(self, job_id) -> dict:
        """
        Retrieves the job parameters for the class diagram chain.
        args:
            job_id (str): The job ID to use.
        returns:
            dict: The job parameters for the class diagram chain.
        """
        if job_id is None:
            raise ValidationError("job_id must be provided.")
        try:
            job_service = JobService()
            job = job_service.get_job_by_id(job_id)
            job_parameters = job.get('parameters', {})
            logger.debug(f"Retrieved job parameters for job_id: {job_id}: {job_parameters}")
            return job_parameters
        except JobNotFoundException as e:
            logger.error(f"Failed to retrieve job parameters for job_id: {job_id}: {e}")
            return {}
    
    def retrieve_analysis_context(self, job_id) -> dict:
        """
        Retrieves the analysis context for the class diagram chain.
        
        args:
            job_id (str): The job ID to use.
        returns:
            dict: The analysis context for the class diagram chain.
        
        Use job_id to retrieve user stories, additional information and pass them into embeddings service to retrieve the analysis context.

        Placeholder for now, but in the future this can be replaced with a call to the embeddings service.
        """
        return {"context": "AWS CloudWatch strongly recommends adding a separate SIT_CAPSTONE_YP class alongside CloudWatch class to monitor the logs. This MUST be incorporated within the diagram."}
    
    def retrieve_audit_criteria(self, job_id) -> dict:
        """
        Retrieves the auditing criteria for the class diagram chain.
        args:
            job_id (str): The job ID to use.
        returns:
            dict: The audit criteria for the class diagram chain.
        
        For now the audit criteria is hardcoded, but in the future it can be retrieved from a database or a configuration file.
        """
        return {
        "audit_criteria_1": "If needed, update the diagram so that each class adheres to the Single Responsibility Principle by having only one reason to change.",
        "audit_criteria_2": "If needed, update the diagram so that classes adhere to the Open/Closed Principle by allowing them to be extended without modifying their existing code.",
        "audit_criteria_3": "If needed, update the diagram so that classes adhere to the Liskov Substitution Principle by being substitutable for their base types without altering the correctness of the program.",
        "audit_criteria_4": "If needed, update the diagram so that Interface Segregation Principle is followed by breaking down large interfaces into smaller, more specific ones.",
        "audit_criteria_5": "If needed, update the diagram so that Dependency Inversion Principle is adhered to by using dependency injection where necessary and ensuring high-level modules do not depend on low-level modules.",
        "audit_criteria_6": "If needed, update the diagram so that classes have their corresponding Views and Controllers when applicable."
        }
