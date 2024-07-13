class ClassDiagramTaskError(Exception):
    def __init__(self, message="Error occurred in ClassDiagramTask"):
        self.error_message = f"ClassDiagramTaskError: {message}"
        super().__init__(self.error_message)

class ClassDiagramConsumerError(Exception):
    def __init__(self, message="Error occurred in ClassDiagramConsumer"):
        self.error_message = f"ClassDiagramConsumerError: {message}"
        super().__init__(self.error_message)
        
class ClassDiagramSignalError(Exception):
    def __init__(self, message="Error occurred in ClassDiagramSignal"):
        self.error_message = f"ClassDiagramSignalError: {message}"
        super().__init__(self.error_message)    

class ERDiagramTaskError(Exception):
    def __init__(self, message="Error occurred in ERDiagramTask"):
        self.error_message = f"ERDiagramTaskError: {message}"
        super().__init__(self.error_message)

class ERDiagramConsumerError(Exception):
    def __init__(self, message="Error occurred in ERDiagramConsumer"):
        self.error_message = f"ERDiagramConsumerError: {message}"
        super().__init__(self.error_message)
        
class ERDiagramSignalError(Exception):
    def __init__(self, message="Error occurred in ERDiagramSignal"):
        self.error_message = f"ERDiagramSignalError: {message}"
        super().__init__(self.error_message)

class DiagramCreationSignalError(Exception):
    def __init__(self, message="Error occurred in Signal"):
        self.error_message = f"DiagramCreationSignalError: {message}"
        super().__init__(self.error_message)