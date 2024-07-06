from abc import ABC
from model_manager.interfaces.BasePromptTemplate import BasePromptTemplate

class BasePromptBuilder(ABC):
    """
    Defines the interface for all prompt builders.
    Prompt builders are used to generate prompts for models or auditors.
    """
    def generate_audit_prompt(prompt_template:BasePromptTemplate, results:dict=None, context:dict=None) -> str:
        """
        Generate an audit prompt based on the results and context.
        args:
            prompt_template (BasePromptTemplate): Prompt template that inherits from BasePromptTemplate.
            results (dict): Results from the model analysis.
            context (dict): Context for the audit.
        """
        pass
    def generate_model_prompt(prompt_template:BasePromptTemplate, job_parameters:dict=None, context:dict=None) -> str:
        """
        Generate a model prompt based on the context.
        args:
            prompt_template (BasePromptTemplate): Prompt template that inherits from BasePromptTemplate.
            job_parameters (dict): The job parameters to be used in the prompt.
            context (dict): Context for the model.
        """
        pass