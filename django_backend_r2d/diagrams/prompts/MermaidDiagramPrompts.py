from model_manager.interfaces.BasePromptTemplate import BasePromptTemplate
from langchain.prompts import PromptTemplate

# Add all analysis prompts related to mermaid diagram generation here

class ClassDiagramPromptTemplate(BasePromptTemplate):
    """
    Prompt used to generate a class diagram based on job_parameters.
    Returns a prompt (str) for generating a class diagram based on the job parameters.
    """    
    @staticmethod
    def get_prompt(job_parameters: dict, context: dict = None) -> str:
        if context is None:
            template = r"""
                You are a systems design expert. Your task is to create comprehensive and detailed class diagrams based on the given user stories.

                Here are the user stories grouped by features:

                {job_parameters}

                Instructions:
                1. Analyze each user story carefully and identify all relevant classes.
                2. Each class should have logical variables (attributes) and functions (methods) that reflect the requirements in the user stories.
                3. Group the class diagrams by features, ensuring each feature and sub-feature has one or more associated classes. Functions within these classes should achieve the described features.
                4. Clearly represent relationships between classes, such as inheritance, composition, and associations.
                5. Use mermaid syntax to express the class diagrams. Ensure that the diagrams are well-structured and easy to understand.
                6. Each class should have a description that explains its purpose, and the user story id it corresponds to.
                
                Syntax for defining classes and attributes:
                classDiagram
                class Square~Shape~{{
                    int id
                    List~int~ position
                    setPoints(List~int~ points)
                    getPoints() List~int~
                }}

                Square : -List~string~ messages
                Square : +setMessages(List~string~ messages)
                Square : +getMessages() List~string~
                Square : +getDistanceMatrix() List~List~int~~

                Syntax for relationships:
                classDiagram
                classA --|> classB : Inheritance
                classC --* classD : Composition
                classE --o classF : Aggregation
                classG --> classH : Association
                classI -- classJ : Link(Solid)
                classK ..> classL : Dependency
                classM ..|> classN : Realization
                classO .. classP : Link(Dashed)
                """  
            prompt = PromptTemplate(
                input_variables=["job_parameters"],
                template=template
            )
            
            return prompt.format(job_parameters=job_parameters)
        else:
            # For prompts where context is provided
            template = """
                You are a systems design expert. Your task is to create class diagrams based on the given user stories.
                Here are the user stories:
                {job_parameters}
                
                Instructions:
                1. Analyze each user story carefully and identify all relevant classes.
                2. Each class must have logical variables (attributes) and functions (methods) that reflect the requirements in the user stories.
                3. Group the class diagrams by features, ensuring each feature and sub-feature has one or more associated classes. Functions within these classes should achieve the described features.
                4. Clearly represent relationships between classes, such as inheritance, composition, and associations.
                5. Use mermaid syntax to express the class diagrams. Ensure that the diagrams are well-structured and easy to understand.
                6. Adapt software design principles and best practices to improve the diagram if necessary.
                7. Here is some additional context that should be incorporated in your design: 
                {context}

                All classes created must have logical variables and functions.
                Group the class diagrams by features. Your output should be one or more class diagrams expressed using mermaid syntax. Ensure that the diagrams are well-structured and clearly represent the relationships between classes.
                """
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