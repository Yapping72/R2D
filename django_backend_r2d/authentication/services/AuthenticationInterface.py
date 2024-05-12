from abc import ABC, abstractmethod

class AuthenticationInterface(ABC):
    """Interface for authentication services to implement"""
    @abstractmethod
    def register(self, data):
        raise NotImplementedError
    @abstractmethod
    def authenticate(self, credentials):
        raise NotImplementedError
