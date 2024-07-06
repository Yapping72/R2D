from abc import ABC, abstractmethod

class BaseDiagramSavingService(ABC):
    """
    Interface that all diagram saving services must implement.
    """
    @abstractmethod
    def save(self, data: dict) -> dict:
        """
        Save the diagram data to the database.
        :param data: dict - The data to be saved.
        :return: dict - The saved data.
        """
        pass