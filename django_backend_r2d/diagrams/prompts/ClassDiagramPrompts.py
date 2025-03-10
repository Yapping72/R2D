from model_manager.interfaces.BasePromptTemplate import BasePromptTemplate
from langchain.prompts import PromptTemplate

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
            2. Each class must have logical variables (attributes) and functions (methods) that reflect the requirements in the user stories. Ensure that all attributes and methods derived from the user stories, including those implicit in the acceptance criteria, are covered.
            3. Group the class diagrams by features, ensuring each feature and sub-feature has one or more associated classes. Functions within these classes should achieve the described features.
            4. Clearly represent relationships between classes, such as inheritance, composition, and associations. All relationships must be labelled, and examples of each relationship type should be included where applicable.
            5. Use mermaid syntax to express the class diagrams. Ensure that the diagrams are well-structured and easy to understand.
            7. Each class must be designed according to SOLID principles, add interface or abstract classes where necessary:
                - Single Responsibility Principle
                - Open/Closed Principle
                - Liskov Substitution Principle
                - Interface Segregation Principle
            8. All relationships MUST BE labelled.
            9. All classes created must have a corresponding controller class, interface class, or view class where necessary:
                - Controller classes handle user input and interact with the main classes.
                - Interface classes define contracts that the main classes implement.
                - View classes represent the user interface components, where applicable.
            10. Each diagram must have a comprehensive description that explains the purpose of each class, its functions and attributes, class relationships, and the user story ID (as denoted in the id field, Do not modify this user story ID) it corresponds to.
            11. Ensure a layered architecture is used where controller, interface, and view classes are necessary.
            12. The user stories you receive will often be incomplete or ambiguous. Use your expertise to fill in the gaps and create a comprehensive class diagram.
                > For example if you see a story related to customers placing orders, you are free to include classes like Cart or Payment to better represent the data model.
                > For example if you see a story related to a login feature, you should extrapolate and create a FailedLoginAttempts class to store the number of failed login attempts. Even if the user stories do not explicitly mention it.
            
            Syntax for defining classes and attributes:
            
            classDiagram
            class Square~Shape~ {{
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
            template = r"""
            You are a systems design expert. Your task is to create comprehensive and detailed class diagrams based on the given user stories.

            Here are the user stories grouped by features:

            {job_parameters}

            Instructions:
            1. Analyze each user story carefully and identify all relevant classes.
            2. Each class must have logical variables (attributes) and functions (methods) that reflect the requirements in the user stories. Ensure that all attributes and methods derived from the user stories, including those implicit in the acceptance criteria, are covered.
            3. Group the class diagrams by features, ensuring each feature and sub-feature has one or more associated classes. Functions within these classes should achieve the described features.
            4. Clearly represent relationships between classes, such as inheritance, composition, and associations. All relationships must be labelled, and examples of each relationship type should be included where applicable.
            5. Use mermaid syntax to express the class diagrams. Ensure that the diagrams are well-structured and easy to understand.
            7. Each class must be designed according to SOLID principles, add interface or abstract classes where necessary:
                - Single Responsibility Principle
                - Open/Closed Principle
                - Liskov Substitution Principle
                - Interface Segregation Principle
            8. All relationships MUST BE labelled.
            9. All classes created must have a corresponding controller class, interface class, or view class where necessary:
                - Controller classes handle user input and interact with the main classes.
                - Interface classes define contracts that the main classes implement.
                - View classes represent the user interface components, where applicable.
            10. Each diagram must have a comprehensive description that explains the purpose of each class, its functions and attributes, class relationships, and the user story ID (as denoted in the id field, Do not modify this user story ID) it corresponds to.
            11. Ensure a layered architecture is used where controller, interface, and view classes are necessary.
            12. The user stories you receive will often be incomplete or ambiguous. Use your expertise to fill in the gaps and create a comprehensive class diagram.
                > For example if you see a story related to customers placing orders, you are free to include classes like Cart or Payment to better represent the data model.
                > For example if you see a story related to a login feature, you should extrapolate and create a FailedLoginAttempts class to store the number of failed login attempts. Even if the user stories do not explicitly mention it.

            Syntax for defining classes and attributes:
            classDiagram
            class Square~Shape~ {{
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
        
            Lastly, here is some additional context:
            {context}
            """
            prompt = PromptTemplate(
                input_variables=["job_parameters", "context"],
                template=template
            )
            
            return prompt.format(job_parameters=job_parameters, context=context)


class AuditClassDiagramPromptTemplate(BasePromptTemplate):
    """
    Prompt used to Audit the class diagrams generated. 
    """
    @staticmethod
    def get_prompt(result: dict, context: dict) -> str:
        template = r"""
            You are a systems design auditor. Your task is to audit the class diagrams generated that have been grouped based on features.

            Here are the class diagrams that need to be audited:
            {result}

            Instructions:
            1. Each diagram must be audited individually. Do not combine multiple diagrams into one.
            2. Check if each diagram correctly represents the requirements from the user stories.
            3. Ensure that all relevant classes, attributes, and methods are present as described in the user stories.
            4. Verify the relationships between classes, including inheritance, composition, and associations.
            5. Ensure that all classes and relationships are logical and necessary for the described functionalities.
            6. Check that the Mermaid syntax is used correctly and the diagrams are well-structured and easy to understand.
            7. Make sure that any additional context or specific instructions provided are incorporated correctly.
            8. Adapt software design principles and best practices to improve the diagrams if necessary.
            10. Each diagram must have a comprehensive description that explains the purpose of each class, its functions and attributes, class relationships, and the user story ID (as denoted in the id field, Do not modify this user story ID) it corresponds to.
            10. Output an improved version of each class diagram. Include any necessary changes, additions, or corrections.
            11. All relationships MUST BE labelled.
            11. Ensure a layered architecture is used where controller, interface, and view classes are necessary.
                > For example if a class diagram is missing a controller class, interface class, or view class, add them where necessary.
                
            Syntax for defining classes and attributes:
            classDiagram
            class Square~Shape~ {{
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
            
            Here are the audit criteria that must be met:
            {context}
            """
        prompt = PromptTemplate(
            input_variables=["result", "context"],
            template=template
        )
        return prompt.format(result=result, context=context)
