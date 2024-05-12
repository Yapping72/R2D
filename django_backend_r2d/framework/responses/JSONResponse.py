from rest_framework.response import Response
from framework.responses.BaseResponse import BaseResponse
from framework.responses.BaseReturnObject import BaseReturnObject
from rest_framework import status

class JSONResponse(BaseResponse):
    """
    Initializes a new instance of JSONResponse with the given properties.

    Args:
        return_object (BaseReturnObject, optional): A BaseReturnObject to initialize the response from.
        Alternatively if return_object is None, JSONResponse accepts data, message, success, and status_code
        data (dict, optional): Data content of the response. Defaults to an empty dictionary.
        message (str, optional): A descriptive message associated with the response. Defaults to an empty string.
        success (bool, optional): Indicates whether the response was successful. Defaults to False.
        status_code (int, optional): HTTP status code to return. Defaults to 500 (Internal Server Error).
    """
    def __init__(self, return_object:BaseReturnObject = None, data: dict={}, message: str ="", success: bool = False, status_code:int = int):
        if isinstance(return_object, BaseReturnObject):
            self.data = return_object.get_data()
            self.message = return_object.get_message()
            self.success = return_object.get_success_status()
            self.status_code = return_object.get_status_code()
        else:
            self.data = data
            self.message = message
            self.success = success
            self.status_code = status_code
            
        self.headers = {}  
        self.headers["HTTP_CODE"] = str(self.status_code)

    def transform(self) -> Response:
        """
        Transforms the JSONResponse object into a Django Rest Framework Response object with appropriate 
        data formatting and HTTP headers.

        Returns:
            Response: A DRF Response object configured with the JSON data, message, status, and HTTP headers.
        
        This method helps in abstracting the response creation process and ensures that all outgoing responses
        are formatted consistently with the necessary HTTP headers.
        """
        # Construct the response data dictionary
        response_data = {
            "data": self.data,
            "message": self.message,
            "success": self.success,
            "status_code": self.status_code
        }
        # Create a DRF Response object with the data, status code, and headers
        response = Response(response_data, status=self.status_code, headers=self.headers)
        return response
