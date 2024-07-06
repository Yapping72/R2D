from rest_framework.exceptions import ValidationError
from enum import Enum

from framework.factories.ModelFactory import ModelFactory
from framework.factories.AuditorFactory import AuditorFactory   
from model_manager.interfaces.BaseModel import BaseModel
from model_manager.interfaces.BaseAuditor import BaseAuditor  
from model_manager.constants import * # Contains the ModelProvider and OpenAIModels enums
from model_manager.services.ModelExceptions import * # Contains the exceptions for the model service
from model_manager.chains.AnalyzeAndAuditChain import AnalyzeAndAuditChain 
from model_manager.chains.AnalyzeAndAuditChainPromptBuilder import AnalyzeAndAuditChainPromptBuilder
from diagrams.chain_inputs.ClassDiagramAuditAnalyzeChainInputs import ClassDiagramAuditAnalyzeChainInputs
from diagrams.interfaces.BaseDiagramService import BaseDiagramService
from diagrams.prompts.MermaidDiagramPrompts import * # Contains the prompt templates for the UML diagrams
from diagrams.prompts.MermaidDiagramAuditorPrompts import *  # Contains the prompt templates for the auditing UML diagrams
from diagrams.prompts.response_schemas import * # Contains the response schemas for the structured output
from diagrams.services.DiagramExceptions import * # Contains the exceptions for the diagram service
from diagrams.serializers.UMLDiagramSerializer import UMLDiagramSerializer
from diagrams.prompts.response_schemas import * # Contains the response schemas for the structured output

import logging 
# Initialize the logger
logger = logging.getLogger('application_logging')

class ClassDiagramService(BaseDiagramService):
    """
    Service that is responsible for creating class diagrams using models and auditing them using auditors.
    """
    def __init__(self, model_factory:ModelFactory, auditor_factory:AuditorFactory, model_provider:ModelProvider, model_name: Enum, auditor_name:Enum):
        self.model_factory = ModelFactory()
        self.auditor_factory = AuditorFactory()
        self.model_provider = model_provider
        self.model_name = model_name
        self.auditor_name = auditor_name
    
    def generate_diagram(self, job_id:str, job_parameters: dict, analysis_context: dict = None) -> dict:
        """
        Generate user stories based on the model name and prompt. 
        Diagrams are generated using the model and auditors provided in the constructor.
        Args:
            job_id: str - The job id for that stores the job_parameters.
            job_parameters: dict - The job parameters to be used in the prompt - concrete BaseJobService classes should return this.
            analysis_context: dict - Additional context to be used in the prompt - concrete BaseEmbeddingService classes should return this.
        Raises: 
            UMLDiagramCreationError - If there is an error in creating the UML diagram.
        """
        try:
            # Validate and deserialize the job_payload using UMLDiagramSerializer
            serializer = UMLDiagramSerializer(data=job_parameters)
            if serializer.is_valid():
                job_parameters = serializer.validated_data['job_parameters']
            else:
                raise ValidationError(serializer.errors)
            
            # Initialize Models
            model = self.model_factory.get_model(self.model_provider, self.model_name)
            auditor = self.auditor_factory.get_auditor(self.model_provider, self.auditor_name)
            
            # Set Audit Criteria here
            audit_criteria = {"audit_criteria_1": "All classes includes base classes to adhere to SOLID principles."}
            
            # Initialize the chain inputs
            chain_inputs = ClassDiagramAuditAnalyzeChainInputs(job_parameters = job_parameters, analysis_context=analysis_context, audit_criteria=audit_criteria)
            
            # Initialize the chain
            chain = AnalyzeAndAuditChain(model, auditor, AnalyzeAndAuditChainPromptBuilder())
            
            # Execute the chain 
            response = chain.execute_chain(chain_inputs)
            logger.debug(f"{response}")
             
            return response
        except ModelInitializationError as e:
            logger.error(f"Failed to initialize Model {e}")
            raise UMLDiagramCreationError(f"Failed to create class diagram for job_id: {job_id}: {e}")
        except ValidationError as e:
            logger.error(f"Failed to validate job_parameters: {e}")
            raise UMLDiagramCreationError(f"Invalid job parameters provided for for job_id: {job_id}: {e}")
        except ModelAnalysisError as e:
            logger.error(f"Failed to analyze prompt: {e}")
            raise UMLDiagramCreationError(f"Encountered errors while processing request: {job_id}: {e}")
        except Exception as e:
            logger.error(f"Unhandled exception encountered: {job_id}: {e}")
            raise UMLDiagramCreationError(f"Unhandled exception encountered: {job_id}: {e}")
    