from model_manager.interfaces.BasePromptTemplate import BasePromptTemplate
from langchain.prompts import PromptTemplate

class ClassDiagramPromptTemplate(BasePromptTemplate):
    """
    Prompt used to generate a class diagram based on job_parameters.
    Returns a prompt (str) for generating a class diagram based on the job parameters.
    """    
    @staticmethod
    def get_prompt(job_parameters: dict, context: dict = None) -> str:
        output_format = {"feature_X": "class diagram in mermaid syntax"}
        if context is None:
            template = """You are a systems design expert, create class diagrams based on the given user stories: {job_parameters}. Group the class diagrams by features, your output should be one or more class diagrams expressed using mermaid syntax. Here is an example of the output format: {output_format}."""
            prompt = PromptTemplate(
                input_variables=["job_parameters"],
                template=template
            )
            return prompt.format(job_parameters=job_parameters)
        else:
            template = """You are a systems design expert, create class diagrams based on the given user stories: {job_parameters}. Here is some additional context: {context}. Group the class diagrams by features, your output should be one or more class diagrams expressed using mermaid syntax. Here is an example of the output format: {output_format}."""
            prompt = PromptTemplate(
                input_variables=["job_parameters", "context"],
                template=template
            )
            return prompt.format(job_parameters=job_parameters, context=context)

class ERDiagramPromptTemplate(BasePromptTemplate):
    """
    Prompt used to generate an ER diagram based on job_parameters.
    Returns a prompt (str) for generating an ER diagram based on the job parameters.
    """
    @staticmethod
    def get_prompt(job_parameters: dict, context: dict = None) -> str:
        if context is None:
            template = """You are a systems design expert, create a ER diagrams based on the given user stories: {job_parameters}. Your output should be in mermaid syntax."""
            prompt = PromptTemplate(
                input_variables=["job_parameters"],
                template=template
            )
            return prompt.format(job_parameters=job_parameters)
        else:
            template = """You are a systems design expert, create ER diagrams based on the given user stories: {job_parameters}. Here is some additional context: {context}. Your output should be in mermaid syntax."""
            prompt = PromptTemplate(
                input_variables=["job_parameters", "context"],
                template=template
            )
            return prompt.format(job_parameters=job_parameters, context=context)

class StateDiagramPromptTemplate(BasePromptTemplate):
    """
    Prompt used to generate a state diagram based on job_parameters.
    Returns a prompt (str) for generating a state diagram based on the job parameters.
    """
    @staticmethod
    def get_prompt(job_parameters: dict, context: dict = None) -> str:
        if context is None:
            template = """You are a systems design expert, create state diagrams based on the given user stories: {job_parameters}. Your output should be in mermaid syntax."""
            prompt = PromptTemplate(
                input_variables=["job_parameters"],
                template=template
            )
            return prompt.format(job_parameters=job_parameters)
        else:
            template = """You are a systems design expert, create state diagrams based on the given user stories: {job_parameters}. Here is some additional context: {context}. Your output should be in mermaid syntax."""
            prompt = PromptTemplate(
                input_variables=["job_parameters", "context"],
                template=template
            )
            return prompt.format(job_parameters=job_parameters, context=context)
        
class SequenceDiagramPromptTemplate(BasePromptTemplate):
    """
    Prompt used to generate a sequence diagram based on job_parameters.
    Returns a prompt (str) for generating a sequence diagram based on the job parameters.
    """
    @staticmethod
    def get_prompt(job_parameters: dict, context: dict = None) -> str:
        if context is None:
            template = """You are a systems design expert, create a ER diagrams based on the given user stories: {job_parameters}. Your output should be in mermaid syntax."""
            prompt = PromptTemplate(
                input_variables=["job_parameters"],
                template=template
            )
            return prompt.format(job_parameters=job_parameters)
        else:
            template = """You are a systems design expert, create a ER diagrams based on the given user stories: {job_parameters}. Here is some additional context: {context}. Your output should be in mermaid syntax."""
            prompt = PromptTemplate(
                input_variables=["job_parameters", "context"],
                template=template
            )
            return prompt.format(job_parameters=job_parameters, context=context)