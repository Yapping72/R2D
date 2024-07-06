from model_manager.interfaces.BasePromptBuilder import BasePromptBuilder
from model_manager.interfaces.BasePromptTemplate import BasePromptTemplate  
from model_manager.services.ModelExceptions import *

class AnalyzeAndAuditChainPromptBuilder(BasePromptBuilder):
    """
    Prompt builder for the Analyze and Audit chain.
    """
    @staticmethod
    def generate_model_prompt(prompt_template:BasePromptTemplate, job_parameters:dict=None, context:dict=None) -> str:
        """
        Generate a model prompt based on the context.
        args:
            prompt_template (BasePromptTemplate): Prompt template that inherits from BasePromptTemplate.
            context (dict): Context for the model.
        raises:
            ModelPromptBuildingError: If the prompt template is not an instance of BasePromptTemplate.
        """
        if not isinstance(prompt_template, BasePromptTemplate):
            raise ModelPromptBuildingError("Model prompt template must inherit from BasePromptTemplate.")
        return prompt_template.get_prompt(job_parameters, context)
    
    @staticmethod
    def generate_audit_prompt(prompt_template:BasePromptTemplate, results:dict=None, context:dict=None) -> str:
        """
        Generate an audit prompt based on the results and context.
        args:
            prompt_template (BasePromptTemplate): Prompt template that inherits from BasePromptTemplate.
            results (dict): Results from the model analysis.
            context (dict): Context for the audit.
        raises:
            AuditPromptBuildingError: If the prompt template is not an instance of BasePromptTemplate or if results are None.
        """    
        if not isinstance(prompt_template, BasePromptTemplate):
            raise AuditPromptBuildingError("Audit prompt template must inherit from BasePromptTemplate.")
        if results is None:
            raise AuditPromptBuildingError("Results are required to generate an audit prompt.")
    
        return prompt_template.get_prompt(results, context)
    
