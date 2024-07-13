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
    def __init__(self, model: BaseModel, auditor: BaseAuditor, chain_input:BaseChainInput, prompt_builder: BasePromptBuilder):
        """
        Analyze and Audit chain supports chaining of responses from a model to an auditor.
        args:
            model (BaseModel): Model to generate a response
            auditor (BaseAuditor): Auditor to audit the response
            chain_input (BaseChainInput): The input object containing the prompts and response schemas.
            prompt_builder (BasePromptBuilder): Prompt builder to generate prompts for the model and auditor.
        """
        self.model = model
        self.auditor = auditor
        self.chain_input = chain_input
        self.prompt_builder = prompt_builder

    def execute_chain(self) -> dict:
        """
        Returns:
            dict: The output dictionary containing the results of each step in the chain.
            example: {analysis_results: {model_response}, audited_results: {auditor_response}
            analysis_results: The results of the model analysis will also contain additional information like model_name_str and is_audited
            audited_results: The results of the auditor analysis will also contain additional information like model_name_str and is_audited
        Raises:
            AnalyzeAndAuditChainException: If there is an error in the chain execution.
        """
        try:
            logger.debug("Running AnalyzeAndAuditChain")
            # Build Model Prompt 
            analysis_prompt = self.prompt_builder.generate_model_prompt(self.chain_input.get_model_prompt_template(), self.chain_input.get_job_parameters(), self.chain_input.get_analysis_context())
            logger.debug(f"Model Prompt: {analysis_prompt}")
            # Run analysis 
            analysis_results = self.model.analyze(analysis_prompt, self.chain_input.get_model_response_schema())
            # Build Audit Prompt using analysis
            audit_prompt = self.prompt_builder.generate_audit_prompt(self.chain_input.get_audit_prompt_template(), analysis_results, self.chain_input.get_audit_criteria())
            logger.debug(f"Audit Prompt: {audit_prompt}")
            # Audit the results
            audited_results = self.auditor.audit(audit_prompt, self.chain_input.get_auditor_response_schema())
            # Store both analysis and audit results in a dictionary
            results = {"analysis_results": analysis_results, "audited_results": audited_results}
            # Append additional information to the results dictionary
            results = self.append_additional_information(results)
            return results
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
            raise AnalyzeAndAuditChainException(f"Unhandled Error while auditing response - {str(e)}")

    def append_additional_information(self, results:dict) -> dict:
        """
        Appends additional information to the results dictionary
        args:
            results (dict): The results dictionary to be appended with additional information.
        returns:
            results (dict): The updated results dictionary.
        """
        # Appends additional information to the results dictionary
        results["analysis_results"]["is_audited"] = False
        results["analysis_results"]["model_name"] = self.model.model_name
        results["audited_results"]["is_audited"] = True
        results["audited_results"]["model_name"] = self.auditor.model_name
        return results
    
    