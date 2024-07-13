from abc import ABC, abstractmethod
import json 
from rest_framework.exceptions import ValidationError
from enum import Enum
from framework.factories.ModelFactory import ModelFactory
from framework.factories.AuditorFactory import AuditorFactory   
from model_manager.interfaces.BaseChainInput import BaseChainInput
from model_manager.interfaces.BasePromptBuilder import BasePromptBuilder
from model_manager.constants import ModelProvider, OpenAIModels
from model_manager.services.ModelExceptions import ModelInitializationError, ModelAnalysisError, AnalyzeAndAuditChainException
from model_manager.chains.AnalyzeAndAuditChain import AnalyzeAndAuditChain 
from jobs.models import Job
from jobs.services.JobExceptions import JobNotFoundException
from diagrams.services.DiagramExceptions import UMLDiagramCreationError
from diagrams.serializers.UMLDiagramSerializer import UMLDiagramSerializer
import logging


# Initialize the logger
logger = logging.getLogger('application_logging')

class BaseDiagramService(ABC):
    """
    Interface that all diagram generating services must implement.
    args:
        model_provider (Enum): The model provider to use.
        model_name (Enum): The model name to use.
        auditor_name (Enum): The auditor name to use.
        chain_input (BaseChainInput): The chain input to use.
        prompt_builder (BasePromptBuilder): The prompt builder to use.
        serializer_class: The serializer class to use.
    """
    def __init__(self, model_provider:Enum, model_name:Enum, auditor_name:Enum, 
                 chain_input:BaseChainInput, prompt_builder:BasePromptBuilder, serializer_class):
        
        self.model_factory = ModelFactory() # Initialize the model factory
        self.auditor_factory = AuditorFactory() # Initialize the auditor factory
        
        # Set the model provider, model name and auditor name
        self.model_provider = model_provider
        self.model_name = model_name
        self.auditor_name = auditor_name
        
        # Set the chain input and prompt builder to use
        self.chain_input = chain_input
        self.prompt_builder = prompt_builder
        
        # Set the serializer class to use
        self.serializer_class = serializer_class
        
    def generate_diagram(self) -> dict:
        """
        Generate user stories based on the model name and prompt. 
        Diagrams are generated using the model and auditors provided in the constructor.
        To add new diagram types create a new service that extends this class, a new chain input class, prompt builder and serializer.
        
        returns:
            chain_response: dict - The response from the chain execution. 
            {"analysis_results": {}, "audited_results": {}}
        raises: 
            UMLDiagramCreationError - If there is an error in creating the UML diagram.
        """
        job_id = self.chain_input.get_job_id()
        
        try:
            # Set the job parameters - Validates the job parameters using the serializer class provided fallback to UMLDiagramSerializer
            self._validate_and_set_job_parameters(self.chain_input.get_job_parameters())
            
            # Initialize Models
            model = self.model_factory.get_model(self.model_provider, self.model_name)
            auditor = self.auditor_factory.get_auditor(self.model_provider, self.auditor_name)
            
            # Set Audit Criteria here - Audit criteria should be set based on the type of diagram being generated
            audit_criteria = self.chain_input.get_audit_criteria()
            
            # Initialize the chain
            chain = AnalyzeAndAuditChain(model, auditor, self.chain_input, self.prompt_builder)
            
            # Execute the chain 
            chain_response = chain.execute_chain()
            logger.debug(f"Chain response: {chain_response}")
            
            return chain_response
        except ModelInitializationError as e:
            logger.error(f"Failed to initialize Model {str(e)}")
            raise UMLDiagramCreationError(f"Failed to create class diagram for job_id: {job_id}: {str(e)}")
        except ValidationError as e:
            logger.error(f"Failed to validate job_parameters: {str(e)}")
            raise UMLDiagramCreationError(f"Invalid job parameters provided for for job_id: {job_id}: {str(e)}")
        except ModelAnalysisError as e:
            logger.error(f"Failed to analyze prompt: {str(e)}")
            raise UMLDiagramCreationError(f"Encountered errors while processing request: {job_id}: {str(e)}")
        except AnalyzeAndAuditChainException as e:
            logger.error(f"Failed to execute chain: {str(e)}")
            raise UMLDiagramCreationError(f"Encountered errors while processing request: {job_id}: {str(e)}")
        except Exception as e:
            logger.error(f"Unhandled exception encountered: {job_id}: {str(e)}")
            raise UMLDiagramCreationError(f"Unhandled exception encountered: {job_id}: {str(e)}")
    
    def _validate_and_set_job_parameters(self, job_parameters: dict):
        """
        Set the job parameters for the chain input.
        Attempts to validate the job parameters using the primary serializer class provided (Create diagrams from previous diagram output).
        If the primary serializer is not valid, it falls back to the UMLDiagramSerializer (Create diagrams from UserStories).
        
        args:
            job_parameters: dict - The job parameters to set.
        """
        # Validate using the primary serializer class provided
        primary_serializer = self.serializer_class(data=job_parameters)
        
        if primary_serializer.is_valid():
            logger.debug("Primary serializer is valid")
            validated_job_parameters = primary_serializer.validated_data
            self.chain_input.set_job_parameters(validated_job_parameters)
            return  # Exit early if primary serializer is valid
        
        # Validate using the UMLDiagramSerializer as a fallback
        fallback_serializer = UMLDiagramSerializer(data=job_parameters)
        
        if fallback_serializer.is_valid():
            logger.debug("UMLDiagramSerializer is valid")
            validated_job_parameters = fallback_serializer.validated_data
            self.chain_input.set_job_parameters(validated_job_parameters)
        else:
            # Raise a validation error if neither serializer is valid
            primary_serializer.is_valid()  # Ensure .is_valid() is called to generate .errors
            raise ValidationError({
                'primary_serializer_errors': primary_serializer.errors,
                'fallback_serializer_errors': fallback_serializer.errors
            })
    
    def retrieve_job_parameters(self, job_id):
        """
        Retrieve job parameters and ensure they are in dictionary format.
        
        Args:
            job_id (str): The job ID.

        Returns:
            dict: The job parameters as a dictionary.

        Raises:
            JobNotFoundException: If the job with the specified ID is not found.
            ValidationError: If the job parameters cannot be decoded from JSON.
        """
        try:
            job = Job.objects.get(job_id=job_id)
            job_parameters_str = job.parameters
        except Job.DoesNotExist:
            raise JobNotFoundException(f"Job with ID {job_id} not found.")
        
        if isinstance(job_parameters_str, dict):
            return job_parameters_str  # Already a dictionary, no need to deserialize
        
        try:
            job_parameters = json.loads(job_parameters_str)
        except json.JSONDecodeError as e:
            raise ValidationError(f"Failed to decode job parameters: {str(e)}")
        
        return job_parameters