from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework import status
from rest_framework.response import Response
from framework.responses.JSONResponse import JSONResponse  
from framework.responses.BaseReturnObject import BaseReturnObject
from framework.responses.SyncAPIReturnObject import SyncAPIReturnObject
from authentication.services.AuthenticationExceptions import *
from jobs.services.JobExceptions import *

import logging
logger = logging.getLogger('application_logging')

class BaseView(APIView):
    def handle_exceptions(func):
        """
        A decorator to standardize response handling and error catching across views.
        Wraps view methods to catch exceptions and convert them into standardized JSON responses.

        Usage:
            @BaseView.handle_exceptions
            def get(self, request, *args, **kwargs):
        """   
        def wrapper(view_instance, request, *args, **kwargs):
            try:
                return_object = func(view_instance, request, *args, **kwargs)
                if not isinstance(return_object, BaseReturnObject):
                    logger.error(f"Parent view did not return an instance of BaseReturnObject")
                    raise ValueError("The view must return an instance of BaseReturnObject")
                return JSONResponse(return_object).transform()
            except serializers.ValidationError as e:
                # Log the error for auditing purposes
                logger.error(f"Serialization Validation error: {str(e)}", exc_info=True)
                return JSONResponse(data = {"error": str(e)}, message ="Validation error during serialization", success = False, status_code=status.HTTP_400_BAD_REQUEST).transform()
            except UserAlreadyExistsError as e:
                logger.error(repr(e), exc_info=True)
                return JSONResponse(data = {"error": str(e)}, message ="Username or email already in use", success = False,  status_code=status.HTTP_400_BAD_REQUEST).transform()
            except JWTTokenGenerationError as e:
                logger.error(repr(e), exc_info=True)
                return JSONResponse(data = {"error": str(e)}, message = "JWT Token Generation Error Could not generate access token for user.", success = False, status_code=status.HTTP_401_UNAUTHORIZED).transform()
            except FailedToCallPwnedAPIError as e:
                logger.error(repr(e), exc_info=True)
                return JSONResponse(data = {"error": str(e)}, message = "Encountered errors while referencing list of leaked passwords", success = False, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR).transform()
            except UsernameFormatError as e:
                logger.error(repr(e), exc_info=True)
                return JSONResponse(data = {"error": str(e)}, message = "Username must at least 8 alphanumeric characters, but not more than 64 characters.",success = False, status_code=status.HTTP_400_BAD_REQUEST).transform()
            except PasswordFormatError as e:
                logger.error(repr(e), exc_info=True)
                return JSONResponse(data = {"error": str(e)}, message = "Password must be at least 12 characters long but not longer than 128 characters.", success = False, status_code=status.HTTP_400_BAD_REQUEST).transform()
            except RegistrationError as e:
                logger.error(repr(e), exc_info=True)
                return JSONResponse(data = {"error": str(e)}, message = "Registration errors were encountered, check that you provided a valid email", success = False, status_code=status.HTTP_400_BAD_REQUEST).transform()
            except AuthenticationError as e:
                logger.error(repr(e), exc_info=True)
                return JSONResponse(data = {"error": str(e)}, message = "Authentication Error", success = False, status_code=status.HTTP_401_UNAUTHORIZED).transform()
            except VerifyPasswordError as e:
                logger.error(repr(e), exc_info=True)
                return JSONResponse(data = {"error": str(e)}, message = "User id or password not provided in payload", success = False, status_code=status.HTTP_400_BAD_REQUEST).transform()
            except UserIDNotFoundError as e: 
                logger.error(repr(e), exc_info=True)
                return JSONResponse(data = {"error": str(e)}, message = "Failed to retrieve User ID or User may not exist", success = False, status_code=status.HTTP_400_BAD_REQUEST).transform()
            except AuthorizationError as e:
                logger.error(repr(e), exc_info=True)
                return JSONResponse(data = {"error": str(e)}, message = "Authorization Error", success = False, status_code=status.HTTP_403_FORBIDDEN).transform()
            except CompromisedPasswordError as e:
                logger.error(repr(e), exc_info=True)
                return JSONResponse(data = {"error": str(e)}, message = "The password you have provided is not secure and has been found in databases of leaked passwords. For your safety, please choose a different password that has not been compromised.", success = False, status_code=status.HTTP_400_BAD_REQUEST).transform()
            except JobCreationException as e:
                logger.error(repr(e), exc_info=True)
                return JSONResponse(data = {"error": str(e)}, message = "Failed to create Job Record", success = False, status_code=status.HTTP_400_BAD_REQUEST).transform()
            except AddToJobQueueException as e:
                logger.error(repr(e), exc_info=True)
                return JSONResponse(data = {"error": str(e)}, message = "Failed to add Job to Job Queue", success = False, status_code=status.HTTP_400_BAD_REQUEST).transform()
            except Exception as e:
                # Log the unexpected error
                logger.error(f"Unhandled exception: {str(e)}", exc_info=True)
                return JSONResponse(data = {"error":f"{str(e)}"}, message = "Internal server error", success = False, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR).transform()
        return wrapper




