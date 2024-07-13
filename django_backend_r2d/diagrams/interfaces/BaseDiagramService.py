from abc import ABC, abstractmethod
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
from diagrams.services.DiagramExceptions import UMLDiagramCreationError
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
            # Validate and deserialize the job_payload using the specified serializer
            serializer = self.serializer_class(data=self.chain_input.get_job_parameters())
            if serializer.is_valid():
                validated_job_parameters = serializer.validated_data['job_parameters']
                self.chain_input.set_job_parameters(validated_job_parameters)
            else:
                raise ValidationError(serializer.errors)
            
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
            logger.error(f"Failed to initialize Model {e}")
            raise UMLDiagramCreationError(f"Failed to create class diagram for job_id: {job_id}: {e}")
        except ValidationError as e:
            logger.error(f"Failed to validate job_parameters: {e}")
            raise UMLDiagramCreationError(f"Invalid job parameters provided for for job_id: {job_id}: {e}")
        except ModelAnalysisError as e:
            logger.error(f"Failed to analyze prompt: {e}")
            raise UMLDiagramCreationError(f"Encountered errors while processing request: {job_id}: {e}")
        except AnalyzeAndAuditChainException as e:
            logger.error(f"Failed to execute chain: {e}")
            raise UMLDiagramCreationError(f"Encountered errors while processing request: {job_id}: {e}")
        except Exception as e:
            logger.error(f"Unhandled exception encountered: {job_id}: {e}")
            raise UMLDiagramCreationError(f"Unhandled exception encountered: {job_id}: {e}")
    

