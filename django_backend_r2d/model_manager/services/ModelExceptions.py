class ModelAPIKeyError(Exception):
    def __init__(self, message="API key was not provided"):
        self.error_message = f"ModelAPIKeyError: {message}"
        super().__init__(self.error_message)

class ModelProviderNotFoundException(Exception):
    def __init__(self, message="Model provider was not found"):
        self.error_message = f"ModelProviderNotFoundException: {message}"
        super().__init__(self.error_message)

class ModelNotFoundException(Exception):
    def __init__(self, message="Model name provided was not found"):
        self.error_message = f"ModelNotFoundException: {message}"
        super().__init__(self.error_message)

class ModelInitializationError(Exception):
    def __init__(self, message="Model initialization error"):
        self.error_message = f"ModelInitializationError: {message}"
        super().__init__(self.error_message)