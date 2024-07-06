from framework.models.BaseAuditor import BaseAuditor
from framework.models.BaseModel import BaseModel
from model_manager.services.ModelExceptions import *
from model_manager.interfaces.BaseChain import BaseChain
from model_manager.interfaces.BasePromptBuilder import BasePromptBuilder
from model_manager.interfaces.BaseChainInput import BaseChainInput

import logging 
# Initialize the logger
logger = logging.getLogger('application_logging')

class AnalyzeAndAuditChain(BaseChain):
    def __init__(self, model: BaseModel, auditor: BaseAuditor, prompt_builder: BasePromptBuilder):
        """
        Analyze and Audit chain supports chaining of responses from a model to an auditor.
        args:
            model (BaseModel): Model to generate a response
            auditor (BaseAuditor): Auditor to audit the response
            prompt_builder (BasePromptBuilder): Prompt builder to generate prompts for the model and auditor.
        """
        self.model = model
        self.auditor = auditor
        self.prompt_builder = prompt_builder
        
    def execute_chain(self, chain_input:BaseChainInput) -> dict:
        """
        Args:
            chain_input (BaseChainInput): The input object containing the prompts and response schemas.
        Returns:
            dict: The output dictionary containing the results of each step in the chain.
        """
        try:
            logger.debug("Running AnalyzeAndAuditChain")
            # Build Model Prompt 
            analysis_prompt = self.prompt_builder.generate_model_prompt(chain_input.get_model_prompt_template(), chain_input.get_analysis_context())
            logger.debug(f"Model Prompt: {analysis_prompt}")
            # Run analysis 
            analysis_results = self.model.analyze(analysis_prompt, chain_input.get_model_response_schema())
            logger.debug(f"Analysis Results: {analysis_results}")
            # Build Audit Prompt using analysis
            audit_prompt = self.prompt_builder.generate_audit_prompt(chain_input.get_audit_prompt_template(), analysis_results, chain_input.get_audit_criteria())
            logger.debug(f"Audit Prompt: {audit_prompt}")
            # Audit the results
            audited_results = self.auditor.audit(audit_prompt, chain_input.get_auditor_response_schema())
            logger.debug(f"Audited Results: {audited_results}")
            return {"analysis_results": analysis_results, "audited_results": audited_results}
        except ModelPromptBuildingError as e:
            raise AnalyzeAndAuditChainException(f"Error while building model prompt - {str(e)}")
        except AuditPromptBuildingError as e:
            raise AnalyzeAndAuditChainException(f"Error while building audit prompt - {str(e)}")
        except ModelAnalysisError as e:
            logger.error(f"Error in AnalyzeAndAuditChain: {str(e)}")
            raise AnalyzeAndAuditChainException(f"Error while generating analysis - {str(e)}")
        except AuditorAnalysisError as e:
            logger.error(f"Error in AnalyzeAndAuditChain: {str(e)}")
            raise AnalyzeAndAuditChainException(f"Error while auditing response - {str(e)}")
        except Exception as e:
            logger.error(f"Error in AnalyzeAndAuditChain: {str(e)}")
            raise e