from model_manager.interfaces.BasePromptTemplate import BasePromptTemplate
from langchain.prompts import PromptTemplate

class ERDiagramPromptTemplate(BasePromptTemplate):
    """
    Prompt used to generate an ER diagram based on job_parameters.
    Returns a prompt (str) for generating a class diagram based on the job parameters.
    """    
    @staticmethod
    def get_prompt(job_parameters: dict, context: dict = None) -> str:
        if context is None:
            template = r"""
            You are a database design expert. Your task is to create comprehensive and detailed entity-relationship (ER) diagrams based on the given features (EPICs), classes, and descriptions.

            Here are the features (EPICs), a description that includes their associations, and classes identified:

            {job_parameters}

            Instructions:
            1. Analyze each class diagram carefully and identify all relevant entities and their relationships.
            2. Each class should be translated into an entity with appropriate attributes.
            3. Ensure that relationships between entities are clearly defined, including primary keys (PK), foreign keys (FK), and cardinality.
            4. Group the ER diagrams by features, ensuring each feature and sub-feature has one or more associated entities.
            5. Use mermaid syntax to express the ER diagrams.
            6. Prioritize CORRECTNESS over conciseness; these diagrams are intended to be used with little to no human intervention or modification.
            7. Each entity should have a description that explains its purpose.
            8. Tables should be normalized and relationships should be well-defined.

            Example of Mermaid Syntax for ER Diagrams:
            erDiagram
                CUSTOMER {
                    string customerId PK
                    string name
                    string email
                }
                ORDER {
                    string orderId PK
                    date orderDate
                    string customerId FK
                }
                CUSTOMER ||--o{ ORDER : places

            Your output should look similar to the example above, with entities and relationships clearly defined.
            """
            prompt = PromptTemplate(
                input_variables=["job_parameters"],
                template=template
            )
            
            return prompt.format(job_parameters=job_parameters)
        else: 
            template = r"""
            You are a database design expert. Your task is to create comprehensive and detailed entity-relationship (ER) diagrams based on the given features (EPICs), classes, and descriptions.

            Here are the features (EPICs), a description that includes their associations, and classes identified:

            {job_parameters}

            Instructions:
            1. Analyze each class diagram carefully and identify all relevant entities and their relationships.
            2. Each class should be translated into an entity with appropriate attributes.
            3. Ensure that relationships between entities are clearly defined, including primary keys (PK), foreign keys (FK), and cardinality.
            4. Group the ER diagrams by features, ensuring each feature and sub-feature has one or more associated entities.
            5. Use mermaid syntax to express the ER diagrams.
            6. Prioritize CORRECTNESS over conciseness; these diagrams are intended to be used with little to no human intervention or modification.
            7. Each entity should have a description that explains its purpose.
            8. Tables should be normalized and relationships should be well-defined.
            
            Example of Mermaid Syntax for ER Diagrams:
            erDiagram
            ENTITY_NAME {
                attribute_type attribute_name PK
                attribute_type attribute_name FK
                attribute_type attribute_name
            }

            Syntax for relationships:
            erDiagram
            ENTITY1 ||--o{ ENTITY2 : Relationship Description
            ENTITY3 ||--|{ ENTITY4 : Another Relationship Description
            ENTITY5 |o--o{ ENTITY6 : Yet Another Relationship Description
            ENTITY7 }|--|{ ENTITY8 : One More Relationship Description

            Your output should look similar to the example above, with entities and relationships clearly defined.
            """
            prompt = PromptTemplate(
                input_variables=["job_parameters", "context"],
                template=template
            )
            
            return prompt.format(job_parameters=job_parameters, context=context)


class AuditERDiagramPromptTemplate(BasePromptTemplate):
    """
    Prompt used to Audit the ER diagrams generated. 
    """
    @staticmethod
    def get_prompt(result: dict, context: dict) -> str:
        template = r"""
        You are a database design auditor. Your task is to audit the provided entity-relationship (ER) diagram and ensure it meets the specified requirements.

        Here is the ER diagram:
        {result}

        Instructions:
        1. Ensure that all relevant entities and their attributes are present.
        2. Verify the relationships between entities, including primary keys, foreign keys, and cardinality.
        3. Ensure that all entities and relationships are logical and necessary for the described functionalities.
        4. Check that the Mermaid syntax is used correctly and the diagram is well-structured and easy to understand.
        5. Make sure that any additional context or specific instructions provided are incorporated correctly.
        6. Adapt database design principles and best practices to improve the diagram if necessary.
        7. Ensure that each entity has a description that explains its purpose and the user story ID it corresponds to.
        8. Tables should be normalized and relationships should be well-defined.

        Here are the audit criteria that must be met:
        {context}

        Syntax for defining entities and attributes:
        erDiagram
            ENTITY_NAME {
                attribute_type attribute_name PK
                attribute_type attribute_name FK
                attribute_type attribute_name
            }

        Syntax for relationships:
        erDiagram
            ENTITY1 ||--o{ ENTITY2 : Relationship Description
            ENTITY3 ||--|{ ENTITY4 : Another Relationship Description
            ENTITY5 |o--o{ ENTITY6 : Yet Another Relationship Description
            ENTITY7 }|--|{ ENTITY8 : One More Relationship Description

        Your final output should be the corrected diagram.
        """
        prompt = PromptTemplate(
            input_variables=["result", "context"],
            template=template
        )
        return prompt.format(result=result, context=context)
