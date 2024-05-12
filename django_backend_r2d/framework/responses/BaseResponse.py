from rest_framework.response import Response
from abc import ABC, abstractmethod
from rest_framework import status

class BaseResponse(ABC):    
    """
    BaseResponse object that all services and controllers will return.
    Mandates the creation of transform to format return values from services / controllers
    """
    @abstractmethod
    def transform(self):
        """
        Services will perform domain logic, and return a BaseResponse Object. This BaseResponse object, 
        will be sent out by controllers and should be formatted for frontend to easily interpret.

        :return: Transformed response object.
        """
        raise NotImplementedError("Subclasses of BaseResponse must implement transform().")
