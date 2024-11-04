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
        
    override the retrieve_job_parameters, retrieve_analysis_context and retrieve_audit_criteria functions to customize the ER diagram chain.
    """
    def __init__(self, model_provider:ModelProvider, model_name: Enum, auditor_name:Enum, job_id:str):
        # Retrieve the job parameters, analysis context and audit criteria
        job_parameters = self.retrieve_job_parameters(job_id)
        analysis_context = self.retrieve_analysis_context(job_id)
        audit_criteria = self.retrieve_audit_criteria(job_id)

        # Initialize the chain input, prompt builder and serializer class
        chain_input = ClassDiagramAuditAnalyzeChainInputs(job_id=job_id, job_parameters=job_parameters, analysis_context=analysis_context, audit_criteria=audit_criteria)
        prompt_builder = AnalyzeAndAuditChainPromptBuilder() # Prompt builder for the Analyze and Audit chain
        serializer_class = UMLDiagramSerializer # Pass the primary serializer class to use
    
        super().__init__(model_provider, model_name, auditor_name, chain_input, prompt_builder, serializer_class)

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
        return {}