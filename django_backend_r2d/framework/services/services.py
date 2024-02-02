from abc import ABC, abstractmethod
from framework.response.response import BaseResponse

class BaseService(ABC):
    @abstractmethod
    def get_service_response(self) -> BaseResponse:
        """
        The get_service_response, should tie all business logic that the service will perform. 
        All inheriting services are free to create their own DAOs and invoke other services. 
        Controllers will only interact with services via this function.
        :return: BaseResponse object.
        """
        raise NotImplementedError

