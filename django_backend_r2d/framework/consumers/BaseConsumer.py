from abc import ABC, abstractmethod

class BaseConsumer(ABC):
    """
    Interface that all consumers should implement
    The consumers should use services within its process_record function
    """
    def __init__(self, consumer_name: str):
        self.consumer_name = consumer_name
        
    @abstractmethod
    def process_record(self, record: dict) -> dict:
        """
        Process a record and return the result.
        
        :param record: The record to process
        :return: The result of processing the record
        """
        pass