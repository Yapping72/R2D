from abc import ABC, abstractmethod

class TokenInterface(ABC):
    """Interface for token providers to implement"""
    @abstractmethod
    def generate_token(self, data):
        raise NotImplementedError

    @abstractmethod
    def extract_user_id(request) -> int:
        """Method that extracts user_id from a token implementation"""
        raise NotImplementedError