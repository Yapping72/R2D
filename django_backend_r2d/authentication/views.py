from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.throttling import UserRateThrottle
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist  
from datetime import datetime
from django.utils.timezone import make_aware
from django.utils import timezone
from django.core.cache import cache
from io import BytesIO
import json
import base64

from authentication.services.AuthenticationService import AuthenticationService
from authentication.services.OTPAuthenticator import OTPAuthenticator
from authentication.services.JWTTokenService import JWTTokenService
from authentication.services.Serializers import UserSerializer
from authentication.services.AuthenticationExceptions import AuthenticationError, RegistrationError, UserAlreadyExistsError, JWTTokenGenerationError, UserIDNotFoundError, FailedToCallPwnedAPIError, VerifyPasswordError
from authentication.services.OTPService import OTPService
from notification.services.SendGridEmailService import SendGridEmailService
from framework.views.BaseView import BaseView
from framework.responses.SyncAPIReturnObject import SyncAPIReturnObject
from framework.utils.EmailHandler import EmailHandler

import logging
logger = logging.getLogger('application_logging')
from django.contrib.auth import get_user_model
User = get_user_model()

otp_service = OTPService() # To handle OTP generation and user association
token_service = JWTTokenService() # To generate JWT Tokens
notification = SendGridEmailService() # To send emails 
otp_authenticator = OTPAuthenticator(otp_service, notification) # To handle OTP authentication
auth_service = AuthenticationService(serializer_class=UserSerializer, otp_authenticator=otp_authenticator) # To authenticate user

class SignUpView(BaseView):
    @BaseView.handle_exceptions
    def post(self, request):
        """
        Creates the user account and registers them if the account is valid.
        Returns access token for users that are successfully registered 
        """
        logger.debug("api/signup invoked")
        user = auth_service.register(request.data)
        access_token = token_service.generate_token(user)
        return SyncAPIReturnObject(
            data = {"access_token": access_token}, 
            message = "User account creation was successful",  
            success = True, 
            status_code = status.HTTP_200_OK)
            
class LoginView(APIView):
    @BaseView.handle_exceptions
    def post(self, request):
        """
        On successful login, the OTP flow is triggered.
        User.id is returned to Frontend 
        """
        logger.debug("api/login invoked")
        username = request.data.get('username')
        password = request.data.get('password')
        user, otp = auth_service.authenticate(username, password) # retrieve the user object and the otp 
        return SyncAPIReturnObject(
            data = {'user_id': user.id, 'user_email': EmailHandler.mask_email(user.email) }, 
            message = "Please verify your OTP", 
            success = True, 
            status_code = status.HTTP_200_OK)
        
class VerifyPassword(APIView):
    permission_classes = [IsAuthenticated]
    @BaseView.handle_exceptions
    def post(self, request):
        logger.debug("api/verify invoked")
        user_id = token_service.extract_user_id(request)  # Safe extraction of user_id from jwt and not from payload
        password = request.data.get('password')
        if not user_id or not password:
            raise VerifyPasswordError
        
        # Use the verify_password method to check the provided password
        auth_service.verify_password(user_id, password)
        return SyncAPIReturnObject(
            data = {'result': True }, 
            message = "Your password has been verified",
            success = True,
            status_code=status.HTTP_200_OK)
        
class RefreshAccessTokenView(APIView):
    """Call this endpoint to refresh a users access token"""
    permission_classes = [IsAuthenticated]
    @BaseView.handle_exceptions
    def post(self, request):
        logger.debug("api/refresh invoked")
        access_token = request.headers.get('Authorization', '')
        user = request.user
        response = token_service.refresh_access_token(user, access_token)
        logger.log(logging.INFO, f"Successfully refreshed access token for user {user.id}")
        logger.log(logging.DEBUG, f"Access token: {response}")
        return SyncAPIReturnObject(
                data = {"access_token": response},
                message = "Successfully Refreshed Access Token",
                success = True,
                status_code=status.HTTP_200_OK)
                
        
class VerifyOTPView(APIView):
    """Call this endpoint to check if a user provided the correct OTP"""
    @BaseView.handle_exceptions
    def post(self, request):
        user_id = request.data.get('user_id')  
        provided_otp = request.data.get('otp')
        user = User.objects.get(pk=user_id)  
        logger.debug("api/otp invoked")
        # Verify the OTP
        is_valid = otp_authenticator.authenticate(user_id = user.id, provided_otp=provided_otp)
        if is_valid:
            access_token = token_service.generate_token(user)
            user.last_login = timezone.now()
            user.save() # Update the last login time of user
            return SyncAPIReturnObject(
                data={'access_token': str(access_token)},
                message="OTP Successfully verified, redirecting you to webpage.",
                success=True,
                status_code=status.HTTP_200_OK)
        else:
            if user is not None:
                raise AuthenticationError("Invalid OTP.")

