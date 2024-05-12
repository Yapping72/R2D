from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import OutstandingToken
from django.test import Client

from authentication.services.TokenInterface import TokenInterface
from authentication.services.AuthenticationExceptions import JWTTokenGenerationError, AuthenticationError, UserIDNotFoundError
from authentication.services.Serializers import CustomTokenPairSerializer

class JWTTokenService(TokenInterface):
    def __init__(self):
        self.base_url = "http://localhost:8000/"
        self.get_new_access_token_endpoint = f"{self.base_url}api/token/refresh/"

    def generate_token(self, user) -> str:
        """Creates refresh token for user and returns an access token"""
        if not user.is_authenticated:
            raise JWTTokenGenerationError("User must be authenticated to generate a token.")
        try:
            self.invalidate_previous_tokens(user) # Blacklist all other outstanding tokens, this way only 1 concurrent user.
            # Add custom claims before generating the token
            refresh_token = CustomTokenPairSerializer.get_token(user)
            return str(refresh_token.access_token)
        except Exception as e:
            raise JWTTokenGenerationError(f"Error generating access token: {e}")

    def refresh_access_token(self, user, auth_header) -> str:
        """
        Refresh the users access token.
        Retrieves the most-recent refresh token for the user.
        Retrieves an access token using this refresh token by making a call to the /token/refresh endpoint.
        """
        if not user.is_authenticated:
            raise JWTTokenGenerationError("User must be authenticated to refresh a token.")

        try:
            # Retrieve the user's outstanding token from the database
            outstanding_token = OutstandingToken.objects.filter(user_id=user.id).order_by('-created_at').first()

            if not outstanding_token:
                raise AuthenticationError("Outstanding token not found for the user.")

            # Verify that the refresh token has not been blacklisted
            if BlacklistedToken.objects.filter(token_id=outstanding_token.id).exists():
                raise AuthenticationError("Refresh token has been blacklisted.")

            refresh_token = str(outstanding_token.token)
            payload = {"refresh": refresh_token} 

            return self._refresh_token(payload, auth_header)

        except TokenError as e:
            raise JWTTokenGenerationError(f"Error refreshing access token: {e}")
        except AuthenticationError as e:
            raise AuthenticationError(e.error_message)
        except JWTTokenGenerationError as e:
            raise JWTTokenGenerationError(e.error_message)

    def _refresh_token(self, payload, access_token):
        # Initialize the test client
        client = Client()
        
        header = {
            "Authorization": access_token,  
            "Content-Type": "application/json"
        }

        # Call the api/token/refresh endpoint to obtain a new access token
        try: 
            response = client.post(
                self.get_new_access_token_endpoint,
                data=payload,
                content_type="application/json",
                **header,
            )
            if response.status_code != 200:
                raise JWTTokenGenerationError(f"Unexpected response code {response.status_code}. Content: {response.content}")

            return str(response.data["access"])
        except (AttributeError, ValueError, KeyError, JWTTokenGenerationError) as e:
            raise JWTTokenGenerationError(f"Error extracting access token. Content: {response.content}")  
    
    def extract_user_id(self,request) -> int:
        """
        Retrieves the user_id from the request object
        Returns user_id (int) if token is valid.
        Raises AuthenticationError or UserIDNotFoundError.
        """
        if request.user.is_anonymous:
            raise AuthenticationError("User is not authenticated.")

        # Extract user_id from the jwt access token 
        try:
            if not request.user.id:
                raise UserIDNotFoundError("The user is authenticated but doesn't have an associated ID.")
            return request.user.id
        except AttributeError:
            raise UserIDNotFoundError()
    
    def invalidate_previous_tokens(self, user):
        """Invalidates all outstanding tokens for the given user."""
        tokens = OutstandingToken.objects.filter(user_id=user.id)
        for token in tokens:
            try:
                # blacklist the Refresh token
                refresh_token = RefreshToken(token=token.token)
                refresh_token.blacklist()
            except Exception as e:
                print(f"Error blacklisting token: {e}")

    