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

from django.contrib.auth import get_user_model
User = get_user_model()


from authentication.services.AuthenticationService import AuthenticationService
from authentication.services.OTPAuthenticator import OTPAuthenticator
from authentication.services.JWTTokenService import JWTTokenService
from authentication.services.Serializers import UserSerializer
from authentication.services.AuthenticationExceptions import AuthenticationError, RegistrationError, UserAlreadyExistsError, JWTTokenGenerationError, UserIDNotFoundError
from authentication.services.OTPService import OTPService
from notification.services.SendGridEmailService import SendGridEmailService
import base64

otp_service = OTPService() # To handle OTP generation and user association
token_service = JWTTokenService() # To generate JWT Tokens
notification = SendGridEmailService()
otp_authenticator = OTPAuthenticator(otp_service, notification) # To handle OTP authentication
auth_service = AuthenticationService(serializer_class=UserSerializer, otp_authenticator=otp_authenticator) # To authenticate user

class SignUpView(APIView):
    def post(self, request):
        """Creates the user account and registers them if the account is valid."""
        try:
            user, private_key = auth_service.register(request.data)
            access_token = token_service.generate_token(user)
            return Response({'access_token': str(access_token),"private_key":private_key}, status=status.HTTP_200_OK)
        
        except UserAlreadyExistsError as e:
            return Response({'error': e.error_message}, status=status.HTTP_400_BAD_REQUEST)
        except JWTTokenGenerationError as e:
            return Response({'error': e.error_message}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({'error': f'An unexpected error occurred {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class LoginView(APIView):
    def post(self, request):
        """On successful login, encrypted user_id will be sent to frontend and an OTP will be generated."""
        username = request.data.get('username')
        password = request.data.get('password')
        try:
            user, otp = auth_service.authenticate(username, password) # retrieve the user object and the otp 
            return Response({'user_id': user.user_id, "details": "Please verify OTP"}, status=status.HTTP_200_OK)
        except AuthenticationError as e:
            return Response({'error': e.error_message}, status=status.HTTP_401_UNAUTHORIZED)
        
class HomeView(APIView): 
    permission_classes = [IsAuthenticated] 
    def get(self, request):
        if request.user.is_authenticated:
            message = f"Congratulations you are logged in {request.user}"
            name = f"{request.user}"
        else:
            message = f"Not authenticated"
        data = {"message": message,"name":name}
        return Response(data)

class VerifyPassword(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            user_id = token_service.extract_user_id(request)
            password = request.data.get('password')
            if not user_id or not password:
                return Response({'error': 'user_id and password are required'}, status=status.HTTP_400_BAD_REQUEST)
            
            # Use the verify_password method to check the provided password
            auth_service.verify_password(user_id, password)
            return Response({'error': 'Password verified successfully'}, status=status.HTTP_200_OK)
        
        except (AuthenticationError, UserIDNotFoundError) as e:
            return Response({'error': f"{e.error_message}"}, status=status.HTTP_401_UNAUTHORIZED)

class RefreshAccessTokenView(APIView):
    """Call this endpoint to refresh a users access token"""
    permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            access_token = request.headers.get('Authorization', '')
            user = request.user
            response = token_service.refresh_access_token(user, access_token)
            return Response({"access_token": response})
        except (AuthenticationError, JWTTokenGenerationError) as e:
            return Response({'error': f"{e.error_message}"}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            print(e.error_message)
            return Response({'error': f"{e.error_message}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class VerifyOTPView(APIView):
    """Call this endpoint to check if a user provided the correct OTP"""
    def post(self, request):
        user_id = request.data.get('user_id')  
        provided_otp = request.data.get('otp')
        decrypted_user_id = user_id_encryption_engine.decrypt(user_id)
        try:
            user = User.objects.get(pk=decrypted_user_id)  
            # Verify the OTP
            is_valid = otp_authenticator.authenticate(user_id = user.id, provided_otp=provided_otp)
            if is_valid:
                access_token = token_service.generate_token(user)
                user.last_login = timezone.now()
                user.save() # Update the last login time of user
                return Response({'access_token': str(access_token)}, status=status.HTTP_200_OK)
            else:
                if user is not None:
                    raise AuthenticationError("Invalid OTP.")

        except AuthenticationError as e:
            return Response({'error': str(e)}, status=status.HTTP_401_UNAUTHORIZED)
        except JWTTokenGenerationError as e:
            return Response({'error': e.error_message}, status=status.HTTP_401_UNAUTHORIZED)
