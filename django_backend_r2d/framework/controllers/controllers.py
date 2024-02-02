from rest_framework.views import APIView
from framework.responses.responses import JSONResponse  # Import your BaseResponse class here

class BaseController(APIView):
    def handle_exceptions(self, func):
        """
        A decorator method to handle exceptions raised by components.
        """
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except serializers.ValidationError as e:
                # Handle validation errors raised by the BaseValidator
                response = JSONResponse({"error": str(e)}, "Validation Error During Serialization", "error", status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                # Handle other unexpected errors
                response = JSONResponse({"error": f"An unexpected error occurred. {str(e)}"}, "Internal Server Error", "error", status.HTTP_500_INTERNAL_SERVER_ERROR)
            return response.transform()  # Transform the BaseResponse object into a DRF Response
        return wrapper