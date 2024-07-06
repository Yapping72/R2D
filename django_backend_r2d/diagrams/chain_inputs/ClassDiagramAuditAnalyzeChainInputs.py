from model_manager.interfaces.BaseChainInput import BaseChainInput
from diagrams.prompts.MermaidDiagramPrompts import ClassDiagramPromptTemplate
from diagrams.prompts.MermaidDiagramAuditorPrompts import AuditClassDiagramPromptTemplate
from diagrams.prompts.response_schemas import MERMAID_CLASS_DIAGRAM_SCHEMA

class ClassDiagramAuditAnalyzeChainInputs(BaseChainInput): 
    """
    Contains the classes and inputs needed to generate class diagrams and audit them.
    args:
        model_prompt_template (ClassDiagramPromptTemplate): Prompt template for the model.
        job_parameters (dict): The job parameters to be used in the prompt.
        audit_prompt_template (AuditClassDiagramPromptTemplate): Prompt template for the auditor.
        analysis_context (dict): Optional Context for the model.
        audit_criteria (dict): Optional Criteria for the audit.
        model_response_schema (Pydantic Model, dict): Optional Schema for the model response.
        auditor_response_schema (Pydantic Model, dict): Optional Schema for the auditor response.
    """ 
    def __init__(self, job_parameters:dict=None, model_prompt_template=ClassDiagramPromptTemplate(), audit_prompt_template=AuditClassDiagramPromptTemplate(), analysis_context=None, audit_criteria=None, model_response_schema=MERMAID_CLASS_DIAGRAM_SCHEMA, auditor_response_schema=MERMAID_CLASS_DIAGRAM_SCHEMA):
        """
        Initialize the chain inputs for the class diagram chain.
        """
        super().__init__(job_parameters, model_prompt_template, audit_prompt_template, analysis_context, audit_criteria, model_response_schema, auditor_response_schema)