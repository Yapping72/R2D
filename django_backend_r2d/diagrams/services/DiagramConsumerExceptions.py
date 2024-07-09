class ClassDiagramTaskError(Exception):
    def __init__(self, message="Error occurred in ClassDiagramTask"):
        self.error_message = f"ClassDiagramTaskError: {message}"
        super().__init__(self.error_message)

class ClassDiagramConsumerError(Exception):
    def __init__(self, message="Error occurred in ClassDiagramConsumer"):
        self.error_message = f"ClassDiagramConsumerError: {message}"
        super().__init__(self.error_message)
