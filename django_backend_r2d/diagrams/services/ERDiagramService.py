from enum import Enum 
from model_manager.constants import ModelProvider # Contains the ModelProvider and OpenAIModels enums
from model_manager.chains.AnalyzeAndAuditChainPromptBuilder import AnalyzeAndAuditChainPromptBuilder
from diagrams.chain_inputs.ClassDiagramAuditAnalyzeChainInputs import ClassDiagramAuditAnalyzeChainInputs
from diagrams.interfaces.BaseDiagramService import BaseDiagramService
from diagrams.serializers.UMLDiagramSerializer import UMLDiagramSerializer
from jobs.services.JobService import JobService

import logging 
# Initialize the logger
logger = logging.getLogger('application_logging')

class ERDiagramService(BaseDiagramService):
    """
    Service class for generating ER diagrams and auditing them.
    Provides a concrete implementation of the BaseDiagramService class.
    Retrieves the job parameters, analysis context and audit criteria for the ER diagram chain.
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
        Retrieves the job parameters for the er diagram chain.
        args:
            job_id (str): The job ID to use.
        returns:
            dict: The job parameters for the er diagram chain.
        """
        if job_id is None:
            raise ValidationError("job_id must be provided.")
        try:
            # Check if job_id exists in ClassDiagrams if so this job is from a secondary step
            job_service = JobService()
            job = job_service.get_job_by_id(job_id)
            job_parameters = job.get('parameters', {})
            logger.debug(f"Retrieved job parameters for job_id: {job_id}: {job_parameters}")
            # If job_id does not exist in ClassDiagrams table, pass in user stories instead
            
            return job_parameters
        except JobNotFoundException as e:
            logger.error(f"Failed to retrieve job parameters for job_id: {job_id}: {e}")
            return {}
    
    def retrieve_analysis_context(self, job_id) -> dict:
        """
        Retrieves the analysis context for the er diagram chain.
        
        args:
            job_id (str): The job ID to use.
        returns:
            dict: The analysis context for the er diagram chain.
        
        Use job_id to retrieve user stories, additional information and pass them into embeddings service to retrieve the analysis context.
        Placeholder for now
        """
        return {"context": "AWS CloudWatch strongly recommends adding a separate SIT_CAPSTONE_YP entity alongside CloudWatch class to monitor the logs. This MUST be incorporated within the diagram."}
    
    def retrieve_audit_criteria(self, job_id) -> dict:
        """
        Retrieves the auditing criteria for the er diagram chain.
        args:
            job_id (str): The job ID to use.
        returns:
            dict: The audit criteria for the er diagram chain.
        
        For now the audit criteria is hardcoded, but in the future it can be retrieved from a database or a configuration file.
        """
        return {"audit_criteria_1: ER Diagrams must be normalized whenever possible."}
    
