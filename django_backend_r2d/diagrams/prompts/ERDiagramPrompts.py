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
            You are a database design expert, your task is to create comprehensive and detailed entity-relationship diagrams. 
            
            You will be provided with job parameters that can be either: 
            1. User stories grouped according to their features. OR
            2. A list of classes, the feature they belong to, and an accompanying description of what each class does.
            
            Regardless of the input provided, you are to identify all relevant entities and their relationships, ensuring that each class is translated into an entity with appropriate attributes.
            
            Here are the job parameters: 
            {job_parameters}

            Instructions:
            1. Analyze the job parameters provided and identify all relevant entities and their relationships.
            2. Each class or story should be translated into an entity with appropriate attributes.
            3. Ensure that relationships between entities are clearly defined, including primary keys (PK), foreign keys (FK), and cardinality.
            4. Group the ER diagrams by features, ensuring each feature and sub-feature has one or more associated entities.
            5. Use mermaid syntax to express the ER diagrams.
            6. Prioritize CORRECTNESS over conciseness; these diagrams are intended to be used with little to no human intervention or modification.
            7. Each entity should have a comprehensive description that explains what the entity represents, its purpose, and the user story or feature it corresponds to.
            8. Tables should be normalized and relationships should be well-defined.
            9. Ensure the entities and attributes are named meaningfully and consistently.

            Example of Mermaid Syntax for ER Diagrams:
            erDiagram
                CUSTOMER {{
                    string customerId PK
                    string name
                    string email
                }}
                ORDER {{
                    string orderId PK
                    date orderDate
                    string customerId FK
                }}
                CUSTOMER ||--o{{ ORDER : places
            """
            # Create the prompt template without context
            prompt = PromptTemplate(
                input_variables=["job_parameters"],
                template=template
            )
            
            return prompt.format(job_parameters=job_parameters)
        else: 
            # Create the prompt template with context
            template = r"""
            You are a database design expert, your task is to create comprehensive and detailed entity-relationship (ER) diagrams. 
            
            You will be provided with job parameters that can be either: 
            1. User stories. OR
            2. A list of classes, the feature they belong to, and an accompanying description of what each class does.
            
            Regardless of the input provided, you are to identify all relevant entities and their relationships, ensuring that each class is translated into an entity with appropriate attributes.
            
            Here are the job parameters: 
            {job_parameters}

            Instructions:
            1. Analyze the job parameters provided and identify all relevant entities and their relationships.
            2. Each class or story should be translated into an entity with appropriate attributes.
            3. Ensure that relationships between entities are clearly defined, including primary keys (PK), foreign keys (FK), and cardinality.
            4. Group the ER diagrams by features, ensuring each feature and sub-feature has one or more associated entities.
            5. Use mermaid syntax to express the ER diagrams.
            6. Prioritize CORRECTNESS over conciseness; these diagrams are intended to be used with little to no human intervention or modification.
            7. Each entity should have a comprehensive description that explains what the entity represents, its purpose, and the user story or feature it corresponds to.
            8. Tables should be normalized and relationships should be well-defined.
            9. Ensure the entities and attributes are named meaningfully and consistently.
  
            Example of Mermaid Syntax for ER Diagrams:
            erDiagram
            ENTITY_NAME {{
                attribute_type attribute_name PK
                attribute_type attribute_name FK
                attribute_type attribute_name
            }}

            Syntax for relationships:
            erDiagram
            ENTITY1 ||--o{{ ENTITY2 : Relationship Description
            ENTITY3 ||--|{{ ENTITY4 : Another Relationship Description
            ENTITY5 |o--o{{ ENTITY6 : Yet Another Relationship Description
            ENTITY7 }}--|{{ ENTITY8 : One More Relationship Description

            Your output should look similar to the example above, with entities and relationships clearly defined.
            
            Here are some additional context for the job:
            {context}
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
        You are a database design auditor. Your task is to audit the provided entity-relationship (ER) diagram that has been grouped based on features.

        Here are the ER diagrams that need to be audited:
        {result}

        Instructions:
        1. Each diagram must be audited individually. Do not combine multiple diagrams into one.
        2. Ensure that all relevant entities and their attributes are present.
        3. Verify the relationships between entities, including primary keys, foreign keys, and cardinality.
        4. Ensure that all entities and relationships are logical and necessary for the described functionalities.
        5. Check that the Mermaid syntax is used correctly and the diagram is well-structured and easy to understand.
        6. Make sure that any additional context or specific instructions provided are incorporated correctly.
        7. Adapt database design principles and best practices to improve the diagram if necessary.
        8. Ensure that each entity has a comprehensive description that explains its purpose and the user story or feature it corresponds to.
        9. Tables should be normalized and relationships should be well-defined.
        10. All accompanying descriptions must be comprehensive and add value in understanding the diagram.

        Here are the audit criteria that must be met:
        {context}

        Syntax for defining entities and attributes:
        erDiagram
            ENTITY_NAME {{
                attribute_type attribute_name PK
                attribute_type attribute_name FK
                attribute_type attribute_name
            }}

        Syntax for relationships:
        erDiagram
            ENTITY1 ||--o{{ ENTITY2 : Relationship Description
            ENTITY3 ||--|{{ ENTITY4 : Another Relationship Description
            ENTITY5 |o--o{{ ENTITY6 : Yet Another Relationship Description
            ENTITY7 }}--|{{ ENTITY8 : One More Relationship Description
        """
        prompt = PromptTemplate(
            input_variables=["result", "context"],
            template=template
        )
        return prompt.format(result=result, context=context)
