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

                Here are the inputs grouped by features:

                {job_parameters}

                Instructions:
                1. Analyze each input carefully and identify all relevant actors and interactions.
                2. Each sequence diagram should depict the flow of messages between actors and objects.
                3. Clearly represent the sequence of interactions, ensuring each step is logical and reflects the requirements.
                4. Use mermaid syntax to express the sequence diagrams. Ensure that the diagrams are well-structured and easy to understand.
                5. Include descriptions for each interaction that explain their purpose and the user story or requirement they correspond to.
                6. Handle alternative flows and loops where applicable, ensuring these are clearly represented in the diagrams.
                7. Ensure that all messages and interactions are labelled with the type of interaction (e.g., message, response, create, delete).
                8. The sequence diagrams must be designed to be production-ready, adhering to best practices in software design.

                Syntax for defining sequence diagrams:
                sequenceDiagram
                actor User
                User ->> Controller: Request
                Controller ->> Service: Process Request
                Service -->> Repository: Save Data
                Repository -->> Service: Data Saved
                Service -->> Controller: Response
                Controller -->> User: Response

                For alternative flows:
                alt Condition
                    User ->> System: Alternative Message
                else Condition
                    User ->> System: Another Alternative Message
                end

                For loops:
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

                Here are the inputs grouped by features:

                {job_parameters}

                Instructions:
                1. Analyze each input carefully and identify all relevant actors and interactions.
                2. Each sequence diagram should depict the flow of messages between actors and objects.
                3. Clearly represent the sequence of interactions, ensuring each step is logical and reflects the requirements.
                4. Use mermaid syntax to express the sequence diagrams. Ensure that the diagrams are well-structured and easy to understand.
                5. Include descriptions for each interaction that explain their purpose and the user story or requirement they correspond to.
                6. Handle alternative flows and loops where applicable, ensuring these are clearly represented in the diagrams.
                7. Ensure that all messages and interactions are labelled with the type of interaction (e.g., message, response, create, delete).
                8. The sequence diagrams must be designed to be production-ready, adhering to best practices in software design.

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

                For alternative flows:
                alt Condition
                    User ->> System: Alternative Message
                else Condition
                    User ->> System: Another Alternative Message
                end

                For loops:
                loop Condition
                    User ->> System: Repeated Message
                end

                Use this syntax to generate the required sequence diagrams:
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
            4. Verify the sequence of messages between actors, including alternative flows and loops.
            5. Ensure that all interactions and messages are logical and necessary for the described functionalities.
            6. Check that the Mermaid syntax is used correctly and the diagrams are well-structured and easy to understand.
            7. Make sure that any additional context or specific instructions provided are incorporated correctly.
            8. Adapt software design principles and best practices to improve the diagrams if necessary.
            9. Each diagram has a description that explains its purpose and the user story, ER diagram, or class diagram it corresponds to.
            10. Output an improved version of each sequence diagram, ensuring the original structure is preserved.
            11. All interactions and messages MUST BE labelled with the type of interaction (e.g., message, response, create, delete).

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

            For alternative flows:
            alt Condition
                User ->> System: Alternative Message
            else Condition
                User ->> System: Another Alternative Message
            end

            For loops:
            loop Condition
                User ->> System: Repeated Message
            end

            Use this syntax to generate the required sequence diagrams:
            """
        prompt = PromptTemplate(
            input_variables=["result", "context"],
            template=template
        )
        return prompt.format(result=result, context=context)