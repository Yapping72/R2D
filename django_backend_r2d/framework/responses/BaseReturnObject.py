from abc import ABC, abstractmethod

class BaseReturnObject(ABC):
    """
    Base class for API response object. Views will be responsible for invoking services. 
    Views will create a BaseReturnObject based on data returned by Services they invoke.

    Args:
        data (dict): The payload to be returned in the response. 
        message (str): A message describing the response or any errors.
        success (bool): Indicates whether the request was successful.
        status_code (int): The HTTP status code for the response. 
    """
    def __init__(self, data, message, success, status_code):
        self.data = data
        self.message = message
        self.success = success
        self.status_code = status_code

    @abstractmethod
    def get_data(self):
        raise NotImplementedError("Subclasses of BaseReturnObject must implement a get_data method")
    
    @abstractmethod
    def get_message(self):
        raise NotImplementedError("Subclasses of BaseReturnObject must implement a get_message method")
    
    @abstractmethod
    def get_success_status(self):
        raise NotImplementedError("Subclasses of BaseReturnObject must implement a get_success_status method")

    @abstractmethod
    def get_status_code(self):
        raise NotImplementedError("Subclasses of BaseReturnObject must implement a get_data method")
