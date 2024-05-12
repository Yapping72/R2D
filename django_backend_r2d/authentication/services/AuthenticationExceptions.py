class AuthenticationError(Exception):
    def __init__(self, message="Unspecified error occurred during authentication."):
        self.error_message = f"AuthenticationError: {message}"
        super().__init__(self.error_message)

class RegistrationError(Exception):
    def __init__(self, message="Unspecified error occurred during registration."):
        self.error_message = f"RegistrationError: {message}"
        super().__init__(self.error_message)

class UserAlreadyExistsError(Exception):
    def __init__(self, message="User Already Exists."):
        self.error_message = f"UserAlreadyExistsError: {message}"
        super().__init__(self.error_message)

class UsernameFormatError(Exception):
    def __init__(self, message="Username must at least 8 alphanumeric characters, but not more than 64 characters."):
        self.error_message = f"UsernameFormatError: {message}"
        super().__init__(self.error_message)

class PasswordFormatError(Exception):
    def __init__(self, message="Password must be at least 12 characters long but not longer than 128 characters."):
        self.error_message = f"PasswordFormatError: {message}"
        super().__init__(self.error_message)

class JWTTokenGenerationError(Exception):
    def __init__(self, message="Unspecified token generation error."):
        self.error_message = f"JWTTokenGenerationError: {message}"
        super().__init__(self.error_message)

class UserIDNotFoundError(Exception):
    def __init__(self, message="Unspecified error while retrieving user id"):
        self.error_message = f"UserIDNotFoundError: {message}"
        super().__init__(self.error_message)

class CompromisedPasswordError(Exception):
    def __init__(self, message="Password is compromised."):
        self.error_message = f"CompromisedPasswordError: {message}"
        super().__init__(self.error_message)

class FailedToCallPwnedAPIError(Exception):
    def __init__(self, message="Unspecified error while retrieving list of pwned passwords"):
        self.error_message = f"FailedToCallPwnedAPIError: {message}"
        super().__init__(self.error_message)

class VerifyPasswordError(Exception):
    def __init__(self, message="Invalid payload, no user_id or password provided"):
        self.error_message = f"VerifyPasswordError: {message}"
        super().__init__(self.error_message)

class AuthorizationError(Exception):
     def __init__(self, message="You are not authorized to perform this action"):
        self.error_message = f"AuthorizationError: {message}"
        super().__init__(self.error_message)

    

