class UMLDiagramCreationError(Exception):
    def __init__(self, message="Failed to create UML diagram"):
        self.error_message = f"UMLDiagramCreationError: {message}"
        super().__init__(self.error_message)

class ClassDiagramSavingError(Exception):
    def __init__(self, message="Failed to save class diagram"):
        self.error_message = f"ClassDiagramSavingError: {message}"
        super().__init__(self.error_message)