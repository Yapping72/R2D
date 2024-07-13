from abc import ABC
from model_manager.interfaces.BasePromptTemplate import BasePromptTemplate
from typing import Optional, Union, Type 
from pydantic import BaseModel as PydanticModel

class BaseChainInput(ABC):
    """
    Base class for storing all the input required for an Analyze-Audit Chain.
    
    args:
        job_id (str): The job ID, used to retrieve the job parameters.
        model_prompt_template (BasePromptTemplate): Prompt template for the model.
        audit_prompt_template (BasePromptTemplate): Prompt template for the auditor.
        job_parameters (dict): The job parameters to be used in the prompt.
        analysis_context (dict, optional): Optional context for the model.
        audit_criteria (dict, optional): Optional criteria for the audit.
        model_response_schema (Union[Type[PydanticModel], dict], optional): Optional schema for the model response.
        auditor_response_schema (Union[Type[PydanticModel], dict], optional): Optional schema for the auditor response.
    functions:
        get_job_parameters: Returns the job parameters.
        set_job_parameters: Sets the job parameters.
        get_model_prompt_template: Returns the model prompt template.
        get_audit_prompt_template: Returns the audit prompt template.
        get_analysis_context: Returns the model context.
        get_audit_criteria: Returns the audit criteria.
        get_model_response_schema: Returns the model response schema.
        get_auditor_response_schema: Returns the auditor response schema.
    """
    def __init__(self, job_id: str, 
                 model_prompt_template: BasePromptTemplate, 
                 audit_prompt_template: BasePromptTemplate, 
                 job_parameters: dict,
                 analysis_context: Optional[dict] = None, 
                 audit_criteria: Optional[dict] = None, 
                 model_response_schema: Optional[Union[Type[PydanticModel], dict]] = None, 
                 auditor_response_schema: Optional[Union[Type[PydanticModel], dict]] = None):
        
        self.job_id = job_id
        self.model_prompt_template = model_prompt_template
        self.audit_prompt_template = audit_prompt_template
        self.job_parameters = job_parameters
        self.analysis_context = analysis_context or {}
        self.audit_criteria = audit_criteria or {}
        self.model_response_schema = model_response_schema
        self.auditor_response_schema = auditor_response_schema
        
    def get_job_id(self) -> str:
        """
        Returns the job ID.
        """
        return self.job_id
    
    def get_job_parameters(self) -> dict:
        """
        Returns the job parameters.
        """
        return self.job_parameters
    
    def set_job_parameters(self, job_parameters:dict):
        """
        Sets the job parameters.
        """
        self.job_parameters = job_parameters
        
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
    