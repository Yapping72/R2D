from model_manager.interfaces.BasePromptTemplate import BasePromptTemplate
from langchain.prompts import PromptTemplate

class SequenceDiagramPromptTemplate(BasePromptTemplate):
    """
    Prompt used to generate a sequence diagram based on job_parameters.
    Returns a prompt (str) for generating a sequence diagram based on the job parameters.
    """
    @staticmethod
    def get_prompt(job_parameters: dict, context: dict = None) -> str:
        if context is None:
            template = r"""
                You are a systems design expert. Your task is to create comprehensive and detailed sequence diagrams based on the given input.

                You will be provided with classes and entities and a summary of what each class/entity does. You need to create sequence diagrams based on the interactions between these classes and entities.

                {job_parameters}

                Instructions:
                1. Analyze each input carefully and identify all relevant actors and interactions.
                2. Each sequence diagram must depict the flow of messages between actors and objects, including primary flows, alternative flows, and loops.
                3. Clearly represent the sequence of interactions, ensuring each step is logical and reflects the requirements.
                4. Use mermaid syntax to express the sequence diagrams. Ensure that the diagrams are well-structured and easy to understand.
                5. Include descriptions for each interaction that explain their purpose and the user story or requirement they correspond to.
                6. Ensure that all messages and interactions are labelled with the type of interaction (e.g., message, response, create, delete).
                7. The sequence diagrams must be designed to be production-ready, adhering to best practices in software design.
                8. Explicitly include all alternative flows and loops in the sequence diagrams. Ensure these are clearly defined and labeled. All alternative flows and loops MUST be part of the mermaid diagram.
                9. The job parameters will often be vague, and you will need to make assumptions based on the information provided. Make smart guesses and feel free to add logical actors and flows where necessary.
                    > For example, you may need to add in Data Access Objects (DAOs) or Service Objects where necessary.
                    > For example, you may need to add a view for a user interface or a database for data storage.
                10. When creating alternative flows and loops, also consider negative scenarios and edge cases that may affect the system.
                    > For example, when describing a primary login flow, a possible alternative flow could be "User enters incorrect password".
            
                Syntax for defining sequence diagrams:
                sequenceDiagram
                actor User
                User ->> Controller: Request
                Controller ->> Service: Process Request
                Service -->> Repository: Save Data
                Repository -->> Service: Data Saved
                Service -->> Controller: Response
                Controller -->> User: Response
                
                alt Condition
                    User ->> System: Alternative Message
                else Condition
                    User ->> System: Another Alternative Message
                end

                loop Condition
                    User ->> System: Repeated Message
                end

                Use this syntax to generate the required sequence diagrams:
                """
            prompt = PromptTemplate(
                input_variables=["job_parameters"],
                template=template
            )
            
            return prompt.format(job_parameters=job_parameters)
        else:
            # For prompts where context is provided
            template = r"""
                You are a systems design expert. Your task is to create comprehensive and detailed sequence diagrams based on the given input.

                You will be provided with classes and entities and a summary of what each class/entity does. You need to create sequence diagrams based on the interactions between these classes and entities.

                {job_parameters}

                Instructions:
                1. Analyze each input carefully and identify all relevant actors and interactions.
                2. Each sequence diagram must depict the flow of messages between actors and objects, including primary flows, alternative flows, and loops.
                3. Clearly represent the sequence of interactions, ensuring each step is logical and reflects the requirements.
                4. Use mermaid syntax to express the sequence diagrams. Ensure that the diagrams are well-structured and easy to understand.
                5. Include descriptions for each interaction that explain their purpose and the user story or requirement they correspond to.
                6. Ensure that all messages and interactions are labelled with the type of interaction (e.g., message, response, create, delete).
                7. The sequence diagrams must be designed to be production-ready, adhering to best practices in software design.
                8. Explicitly include all alternative flows and loops in the sequence diagrams. Ensure these are clearly defined and labeled. All alternative flows and loops MUST be part of the mermaid diagram.
                9. The job parameters will often be vague, and you will need to make assumptions based on the information provided. Make smart guesses and feel free to add logical actors and flows where necessary.
                    > For example, you may need to add in Data Access Objects (DAOs) or Service Objects where necessary.
                    > For example, you may need to add a view for a user interface or a database for data storage.
                10. When creating alternative flows and loops, also consider negative scenarios and edge cases that may affect the system.
                    > For example, when describing a primary login flow, a possible alternative flow could be "User enters incorrect password".

                Lastly here is some additional context:
                {context}

                Syntax for defining sequence diagrams:
                sequenceDiagram
                actor User
                User ->> Controller: Request
                Controller ->> Service: Process Request
                Service -->> Repository: Save Data
                Repository -->> Service: Data Saved
                Service -->> Controller: Response
                Controller -->> User: Response
                
                alt Condition
                    User ->> System: Alternative Message
                else Condition
                    User ->> System: Another Alternative Message
                end

                loop Condition
                    User ->> System: Repeated Message
                end

                Your output should contain one or more sequence diagrams. 
                """
            prompt = PromptTemplate(
                input_variables=["job_parameters", "context"],
                template=template
            )
            
            return prompt.format(job_parameters=job_parameters, context=context)

class AuditSequenceDiagramPromptTemplate(BasePromptTemplate):
    """
    Prompt used to audit the sequence diagrams generated.
    """
    @staticmethod
    def get_prompt(result: dict, context: dict) -> str:
        template = r"""
            You are a systems design auditor. Your task is to audit the sequence diagrams generated based on the given inputs.

            Here are the sequence diagrams that need to be audited:
            {result}

            Instructions:
            1. Each diagram must be audited individually. Do not combine multiple diagrams into one.
            2. Check if each diagram correctly represents the requirements from the user stories, ER diagrams, or class diagrams.
            3. Ensure that all relevant actors and interactions are present as described in the input.
            4. Verify the sequence of messages between actors, including primary flows, alternative flows and loops.
            5. Ensure that all interactions and messages are logical and necessary for the described functionalities.
            6. Check that the Mermaid syntax is used correctly and the diagrams are well-structured and easy to understand.
            7. Make sure that any additional context or specific instructions provided are incorporated correctly.
            8. Adapt software design principles and best practices to improve the diagrams if necessary.
            9. Each diagram has a description that explains its purpose and the user story, ER diagram, or class diagram it corresponds to.
            10. Output an improved version of each sequence diagram, ensuring the original structure is preserved.
            11. All interactions and messages MUST BE labelled with the type of interaction (e.g., message, response, create, delete).
            12. All alternative flows and loops must be clearly defined and labeled in the sequence diagrams.
            13. The job parameters will often be vague, and you will need to make logical assumptions based on the information provided. Make smart guesses and feel free to add logical actors and flows where necessary.
                > For example, you may need to add in Data Access Objects (DAOs) or Service Objects where necessary.
                > For example, you may need to add a view for a user interface or a database for data storage.
            14. All primary flows, alternative flows, actors, messages and loops MUST be part of the Mermaid diagram and not only in the descriptions.
            15. When creating alternative flows and loops, also consider negative scenarios and edge cases that may affect the system.
                > For example, when describing a primary login flow, a possible alternative flow could be "User enters incorrect password".
            16. You must add in alternative flows and loops to the diagram if they are missing. 
            
            Here are the audit criteria that must be met:
            {context}

            Syntax for defining sequence diagrams:
            sequenceDiagram
            actor User
            User ->> Controller: Request
            Controller ->> Service: Process Request
            Service -->> Repository: Save Data
            Repository -->> Service: Data Saved
            Service -->> Controller: Response
            Controller -->> User: Response
            
            alt Condition
                User ->> System: Alternative Message
            else Condition
                User ->> System: Another Alternative Message
            end

            loop Condition
                User ->> System: Repeated Message
            end

            Your output should contain multiple sequence diagrams that have been audited and improved.
            """
        prompt = PromptTemplate(
            input_variables=["result", "context"],
            template=template
        )
        return prompt.format(result=result, context=context)