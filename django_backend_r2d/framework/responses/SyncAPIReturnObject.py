from rest_framework import status
from framework.responses.BaseReturnObject import BaseReturnObject

class SyncAPIReturnObject(BaseReturnObject):
    """
    Initializes an API response object.

    Args:
        data (dict): The payload to be returned in the response. Defaults to an empty dict.
        message (str): A message describing the response or any errors. Defaults to an empty string.
        success (bool): Indicates whether the request was successful. Defaults to False.
        status_code (int): The HTTP status code for the response. Defaults to 500 (Internal Server Error).

    Raises:
        ValueError: If any of the required fields are inappropriately set.
    """
    def __init__(self, data: dict = None, message: str = "", success: bool = False, status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR):
        if data is None:
            data = {}  # Ensure data is always a dictionary

        if not isinstance(data, dict):
            self.logger.error("Invalid Data provided to API Response", exc_info=True)
            raise ValueError("Data must be a dictionary.")

        if not isinstance(message, str):
            self.logger.error("Invalid Message provided to API Response", exc_info=True)
            raise ValueError("Message must be a string.")

        if not isinstance(success, bool):
            self.logger.error("Invalid success provided to API Response", exc_info=True)
            raise ValueError("Success must be a boolean.")

        if not isinstance(status_code, int) or status_code < 100 or status_code > 599:
            self.logger.error("Invalid status_code provided to API Response", exc_info=True)
            raise ValueError("Status code must be a valid HTTP status code between 100 and 599.")

        super().__init__(data, message, success, status_code)
    
    def get_data(self):
        return self.data
    
    def get_message(self):
        return self.message
    
    def get_success_status(self):
        return self.success

    def get_status_code(self):
        return self.status_code
    
