class UMLDiagramCreationError(Exception):
    def __init__(self, message="Failed to create UML diagram"):
        self.error_message = f"UMLDiagramCreationError: {message}"
        super().__init__(self.error_message)

class ClassDiagramSavingError(Exception):
    def __init__(self, message="Failed to save class diagram"):
        self.error_message = f"ClassDiagramSavingError: {message}"
        super().__init__(self.error_message)

class ClassDiagramRetrievalError(Exception):
    def __init__(self, message="Failed to retrieve class diagrams"):
        self.error_message = f"ClassDiagramRetrievalError: {message}"
        super().__init__(self.error_message)

class ERDiagramSavingError(Exception):
    def __init__(self, message="Failed to save ER diagram"):
        self.error_message = f"ERDiagramSavingError: {message}"
        super().__init__(self.error_message)

class ERDiagramRetrievalError(Exception):
    def __init__(self, message="Failed to retrieve ER diagrams"):
        self.error_message = f"ERDiagramRetrievalError: {message}"
        super().__init__(self.error_message)

class SequenceDiagramSavingError(Exception):
    def __init__(self, message="Failed to save sequence diagram"):
        self.error_message = f"SequenceDiagramSavingError: {message}"
        super().__init__(self.error_message)

class SequenceDiagramRetrievalError(Exception):
    def __init__(self, message="Failed to retrieve sequence diagrams"):
        self.error_message = f"SequenceDiagramRetrievalError: {message}"
        super().__init__(self.error_message)
        
class DiagramRepositoryInstantiationError(Exception):
    def __init__(self, message="Failed to retrieve requested repository"):
        self.error_message = f"DiagramRepositoryInstantiationError: {message}"
        super().__init__(self.error_message)