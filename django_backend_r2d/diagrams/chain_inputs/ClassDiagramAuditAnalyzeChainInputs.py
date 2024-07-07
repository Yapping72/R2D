from model_manager.interfaces.BaseChainInput import BaseChainInput
from diagrams.prompts.MermaidDiagramPrompts import ClassDiagramPromptTemplate
from diagrams.prompts.MermaidDiagramAuditorPrompts import AuditClassDiagramPromptTemplate
from diagrams.prompts.response_schemas import MERMAID_CLASS_DIAGRAM_SCHEMA
from jobs.services.JobService import JobService

class ClassDiagramAuditAnalyzeChainInputs(BaseChainInput): 
    """
    Contains the classes and inputs needed to generate class diagrams and audit them.
    
    args:
        job_id (str): The job ID, used to retrieve the job parameters.
        model_prompt_template (ClassDiagramPromptTemplate): Prompt template for the model.
        audit_prompt_template (AuditClassDiagramPromptTemplate): Prompt template for the auditor.
        job_parameters (dict, optional): The job parameters to be used in the prompt.
        analysis_context (dict, optional): Optional context for the model.
        audit_criteria (dict, optional): Optional criteria for the audit.
        model_response_schema (dict, optional): Optional schema for the model response.
        auditor_response_schema (dict, optional): Optional schema for the auditor response.
    
    functions:
        get_job_parameters: Returns the job parameters.
        set_job_parameters: Sets the job parameters.
        get_model_prompt_template: Returns the model prompt template.
        get_audit_prompt_template: Returns the audit prompt template.
        get_analysis_context: Returns the model context.
        get_audit_criteria: Returns the audit criteria.
        get_model_response_schema: Returns the model response schema.
        get_auditor_response_schema: Returns the auditor response schema.
        retrieve_job_parameters: Retrieves the job parameters using the job service.
    """
    def __init__(self, job_id: str, 
                 model_prompt_template: ClassDiagramPromptTemplate = ClassDiagramPromptTemplate(),
                 audit_prompt_template: AuditClassDiagramPromptTemplate = AuditClassDiagramPromptTemplate(),
                 job_parameters: dict = None,
                 analysis_context: dict = None, audit_criteria: dict = None,
                 model_response_schema: dict = MERMAID_CLASS_DIAGRAM_SCHEMA,
                 auditor_response_schema: dict = MERMAID_CLASS_DIAGRAM_SCHEMA):
        """
        Initialize the chain inputs for the class diagram chain.
        """
        super().__init__(job_id=job_id,
                         model_prompt_template=model_prompt_template,
                         audit_prompt_template=audit_prompt_template,
                         job_parameters=job_parameters,
                         analysis_context=analysis_context, audit_criteria=audit_criteria,
                         model_response_schema=model_response_schema,
                         auditor_response_schema=auditor_response_schema)