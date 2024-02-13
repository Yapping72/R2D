from rest_framework.response import Response
from abc import ABC, abstractmethod

class BaseResponse(ABC):    
    @abstractmethod
    def transform(self):
        """
        Services will perform domain logic, and return a BaseResponse Object. This BaseResponse object, 
        will be sent out by controllers and should be formatted for frotnend to easily interpret.

        :return: Transformed response object.
        """
        raise NotImplementedError("Subclasses of BaseResponse must implement transform().")

class JSONResponse(BaseResponse):
    def __init__(self, data: dict, message: str, status: str, status_code: int):
        self.data = data
        self.message = message
        self.status = status
        self.status_code = status_code
        self.headers = {}  
        self.headers["HTTP_CODE"] = str(self.status_code)

    def transform(self) -> Response:
        """
        Transforms service results into a Json Response.

        Example JSON Response Format:
        {
            "data": {
                domain_key_1: domain_value_1
                domain_key_2: domain_value_2 
            },
            "message": str,
            "status": str
        }

        Example HTTP Headers:
        HTTP/1.1 200 OK
        """
        response_data = {
            "data": self.data,
            "message": self.message,
            "status": self.status,
        }
        response = Response(response_data, status=self.status_code, headers=self.headers)
        return response
