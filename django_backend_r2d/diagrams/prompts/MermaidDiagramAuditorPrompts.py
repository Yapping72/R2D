from model_manager.interfaces.BasePromptTemplate import BasePromptTemplate
from langchain.prompts import PromptTemplate

# Add all audit prompts related to auditing mermaid diagram generation here

class AuditClassDiagramPromptTemplate(BasePromptTemplate):
    """
    Prompt used to Audit the class diagrams generated. 
    """
    @staticmethod
    def get_prompt(result: dict, context: dict) -> str:
        template = r"""
        You are a systems design auditor. Your task is to audit the provided class diagram and ensure it meets the specified requirements.

        Here is the class diagram:
        {result}

        Instructions:
        1. Check if the diagram correctly represents the requirements from the user stories.
        2. Ensure that all relevant classes, attributes, and methods are present as described in the user stories.
        3. Verify the relationships between classes, including inheritance, composition, and associations.
        4. Ensure that all classes and relationships are logical and necessary for the described functionalities.
        5. Check that the Mermaid syntax is used correctly and the diagram is well-structured and easy to understand.
        6. Make sure that any additional context or specific instructions provided are incorporated correctly.
        7. Adapt software design principles and best practices to improve the diagram if necessary.
        8. Ensure that each diagram has a description that explains its purpose and the user story ID it corresponds to.

        Here are the audit criteria that must be met:
        {context}

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

        Your final output should be the corrected diagram. 
        """
        prompt = PromptTemplate(
            input_variables=["result", "context"],
            template=template
        )
        return prompt.format(result=result, context=context)
