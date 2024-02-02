from rest_framework.response import Response
from abc import ABC, abstractmethod

class BaseResponse(ABC):    
    @abstractmethod
    def transform(self):
        """
        Transforms the Response object into the desired target format. 

        :return: Transformed response object.
        """
        raise NotImplementedError

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
        Transform the JSONResponse object into a DRF Response object.
        Example JSON Response Format:
        {
            "data": {
                "user_id": int,
                "username": str,
                "email": str
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
