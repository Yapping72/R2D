from abc import ABC, abstractmethod

class BaseRepositoryFactory(ABC):
    @staticmethod
    @abstractmethod
    def get_repository(factory_name:str):
        """Returns the requested repository"""
        raise NotImplementedError("Subclasses of BaseRepositoryFactory must implement get_repository().")

