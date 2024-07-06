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

class ModelAnalysisError(Exception):
    def __init__(self, message="Model initialization error"):
        self.error_message = f"ModelAnalysisError: {message}"
        super().__init__(self.error_message)

class AuditorInitializationError(Exception):
    def __init__(self, message="Auditor initialization error"):
        self.error_message = f"AuditorInitializationError: {message}"
        super().__init__(self.error_message)

class AuditorAnalysisError(Exception):
    def __init__(self, message="Auditor analysis error"):
        self.error_message = f"AuditorAnalysisError: {message}"
        super().__init__(self.error_message)

class AnalyzeAndAuditChainException(Exception):
    def __init__(self, message="Analyze and Audit chain error"):
        self.error_message = f"AnalyzeAndAuditChainException: {message}"
        super().__init__(self.error_message)

class ModelPromptBuildingError(Exception): 
    def __init__(self, message="Model prompt building error"):
        self.error_message = f"ModelPromptBuildingError: {message}"
        super().__init__(self.error_message)

class AuditPromptBuildingError(Exception):
    def __init__(self, message="Audit prompt building error"):
        self.error_message = f"AuditPromptBuildingError: {message}"
        super().__init__(self.error_message)
    