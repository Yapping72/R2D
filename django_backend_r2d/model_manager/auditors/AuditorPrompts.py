from model_manager.interfaces.BasePromptTemplate import BasePromptTemplate
from langchain.prompts import PromptTemplate


class AuditClassDiagramPromptTemplate(BasePromptTemplate):
    """
    Prompt used to generate a class diagram based on job_parameters.
    Returns a prompt (str) for generating a class diagram based on the job parameters.
    """
    @staticmethod
    def get_prompt(job_parameters: dict, context: dict = None) -> str:
        template = """You are a systems design expert, your job is to check that these mermaid diagrams: {job_parameters} is free from syntax errors and meets the acceptance criteria {context}. Your output should be in mermaid syntax."""
        prompt = PromptTemplate(
            input_variables=["job_parameters", "context"],
            template=template
         )
        return prompt.format(job_parameters=job_parameters, context=context)

