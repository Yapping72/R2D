from abc import ABC
from model_manager.interfaces.BasePromptTemplate import BasePromptTemplate

class BaseChainInput(ABC):
    """
    Stores all the input required for a Analyze-Audit Chain.
    Concrete classes can inherit from this class and add additional fields as required.    
    args:
        job_parameters (dict): The job parameters to be used in the prompt.
        model_prompt_template (BasePromptTemplate): Prompt template for the model.
        audit_prompt_template (BasePromptTemplate): Prompt template for the auditor.
        analysis_context (dict): Optional Context for the model.
        audit_criteria (dict): Optional Criteria for the audit.
        model_response_schema (Pydantic Model, dict): Optional Schema for the model response.
        auditor_response_schema (Pydantic Model, dict): Optional Schema for the auditor response.
    functions:
        get_job_parameters: Returns the job parameters.
        get_model_prompt_template: Returns the model prompt template.
        get_audit_prompt_template: Returns the audit prompt template.
        get_analysis_context: Returns the model context.
        get_audit_criteria: Returns the audit criteria.
        get_model_response_schema: Returns the model response schema.
        get_auditor_response_schema: Returns the auditor response schema.
    """
    def __init__(self, job_parameters:dict, model_prompt_template:BasePromptTemplate, audit_prompt_template:BasePromptTemplate, analysis_context=None, audit_criteria=None, model_response_schema=None, auditor_response_schema=None):
        self.job_parameters = job_parameters # The job parameters to be used in the prompt
        self.model_prompt_template = model_prompt_template # Concrete class that inherits from BasePromptTemplate
        self.audit_prompt_template = audit_prompt_template # Concrete class that inherits from BasePromptTemplate 
        self.analysis_context = analysis_context # Optional context for the model
        self.audit_criteria = audit_criteria or {} # Optional criteria for the audit
        self.model_response_schema = model_response_schema # Optional schema for the model response
        self.auditor_response_schema = auditor_response_schema # Optional schema for the auditor response
    
    def get_job_parameters(self) -> dict:
        """
        Returns the job parameters.
        """
        return self.job_parameters
    
    def get_model_prompt_template(self) -> BasePromptTemplate:
        """
        Returns the model prompt template.
        """
        return self.model_prompt_template

    def get_audit_prompt_template(self) -> BasePromptTemplate:
        """
        Returns the audit prompt template.
        """
        return self.audit_prompt_template

    def get_analysis_context(self) -> dict:
        """
        Returns the model context.
        """
        return self.analysis_context

    def get_audit_criteria(self) -> dict:
        """
        Returns the audit criteria.
        """
        return self.audit_criteria

    def get_model_response_schema(self) -> dict:
        """
        Returns the model response schema.
        """
        return self.model_response_schema

    def get_auditor_response_schema(self) -> dict:
        """
        Returns the auditor response schema.
        """
        return self.auditor_response_schema
