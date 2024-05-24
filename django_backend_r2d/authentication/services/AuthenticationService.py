from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.exceptions import ObjectDoesNotExist  
from authentication.services.AuthenticationInterface import AuthenticationInterface
from authentication.services.AuthenticationExceptions import UsernameFormatError, PasswordFormatError, CompromisedPasswordError, AuthorizationError
from authentication.services.AuthenticationExceptions import UserAlreadyExistsError, RegistrationError, AuthenticationError, FailedToCallPwnedAPIError
from authentication.services.OTPAuthenticator import OTPAuthenticator
from authentication.services.OTPInterface import OTPInterface
from django.utils import timezone
from ..models import FailedLoginAttempt
import hashlib
import requests

from django.contrib.auth import get_user_model
User = get_user_model() # Use custom User model instead of Django default user model

import logging 
logger = logging.getLogger("application_logging") # Instantiate logger class

class AuthenticationService(AuthenticationInterface):
    """
    Authentication Service that is responsible for registering and authenticating users.
    The authentication service here registers a user based on username, email and password.
    """
    def __init__(self, serializer_class, otp_authenticator: AuthenticationInterface):
        self.serializer_class = serializer_class
        self.otp_authenticator = otp_authenticator

    def register(self, data:dict):
        logger.debug(f"Registering new user - {data}")
        data['username'] = data.get('username').lower()

        if not self.is_valid_username(data.get('username')):
            raise UsernameFormatError()
        
        if not self.is_valid_password(data.get('password')):
            raise PasswordFormatError()
        
        if(self.is_password_compromised(data.get('password'))):
            raise CompromisedPasswordError()

        # Check if the user already exists based on username or email
        if User.objects.filter(username=data.get('username')).exists():
            raise UserAlreadyExistsError("Username already in use")
        
        if User.objects.filter(email=data.get('email')).exists():
            raise UserAlreadyExistsError("Email already in use")

        # Create a serializer instance with the provided data
        serializer = self.serializer_class(data=data)
        
        # Check if the data is valid according to the serializer's rules
        if serializer.is_valid():
            # Save the user object to the database
            user = serializer.save()
            logger.debug(f"New user registered - ${user.username}")
            # Return the created user object and None for errors
            return user
        # If the data is not valid, return None for the user and the serializer errors
        else:
            raise RegistrationError(serializer.errors)
        
    def is_valid_username(self, username):
        return username.isalnum() and 8 <= len(username) <= 64

    def is_valid_password(self, password):
        return 12 <= len(password) <= 128
    
    def is_password_compromised(self, password):
        # Hash the password using SHA-1
        sha1_password = hashlib.sha1(password.encode()).hexdigest().upper()
        # Split the hashed password into a prefix and a suffix
        prefix, suffix = sha1_password[:5], sha1_password[5:]

        # Send a request to the PwnedPasswords API to check if the password is compromised
        url = f"https://api.pwnedpasswords.com/range/{prefix}"
        response = requests.get(url)

        if response.status_code == 200:
            # Check if the suffix of the hashed password exists in the response
            compromised_passwords = response.text.split('\n')
            for line in compromised_passwords:
                if line.startswith(suffix):
                    return True  # Password is compromised
        else:
            # Handle API request error
            raise FailedToCallPwnedAPIError("Failed to check password against PwnedPasswords API")

        return False  # Password is not compromised

    def authenticate(self, username: str, password: str):
        """
        Authenticate the user with the provided username and password.
        If the user is authenticated (correct username and password), an OTP is sent to the user's EMAIL.
        """
        username = username.lower()
        user = authenticate(username=username, password=password)
        
        if user:
            otp = self.otp_authenticator.register(user)  # Start the 2FA flow.
            logger.debug(f"User details - username: {user.username}, email: {user.email}, first_name: {user.first_name}, last_name: {user.last_name}, role: {user.role}, is_active: {user.is_active}, is_staff: {user.is_staff}, is_superuser: {user.is_superuser}, date_joined: {user.date_joined}, last_login: {user.last_login}")
        else:
            # Capture the user_id from the failed authentication
            user_id = None
            try:
                user = User.objects.get(username=username)
                logger.debug(f"User details - userid = {user.id} username: {user.username}, email: {user.email}, first_name: {user.first_name}, last_name: {user.last_name}, role: {user.role}, is_active: {user.is_active}, is_staff: {user.is_staff}, is_superuser: {user.is_superuser}, date_joined: {user.date_joined}, last_login: {user.last_login}")
                user_id = user.id
            except User.DoesNotExist:
               raise AuthenticationError(f"This user does not exists.")

            if user_id is not None:
                try:
                    stored_failedAttempt, created = FailedLoginAttempt.objects.get_or_create(user_id=user_id)
                    logger.debug(f"Failed counts for user ID [{user_id}] -- {stored_failedAttempt.failed_count}")
                    if stored_failedAttempt.failed_count >= 5:
                        logger.debug("Account Locked")
                        raise AuthenticationError(f"Account has been disabled due to repeated failed login attempts. Please contact system administrator.")
                except FailedLoginAttempt.DoesNotExist:
                    # If row doesn't exist, create a new entry
                    FailedLoginAttempt.objects.create(timestamp=timezone.now(), failed_count=0, user_id=user_id)

                if stored_failedAttempt.check_timestamp():
                    stored_failedAttempt.reset_failed_attempts()
                    stored_failedAttempt.add_failed_attempt()
                else:
                    stored_failedAttempt.add_failed_attempt()
                    if stored_failedAttempt.failed_count >= 5:
                        raise AuthenticationError(f"Account has been disabled due to repeated failed login attempts. Please contact system administrator.")
                    
            raise AuthenticationError(f"Invalid Credentials Provided")
        return user, otp
        
    def verify_password(self, user_id:str, password:str):
        """
        Verify if the provided password matches the password of the user
        with the given user_id.
        """
        try:
            # Retrieve the user object by its ID
            user = User.objects.get(pk=user_id)
            logger.debug(f"Verifying password for {user}")
        except User.DoesNotExist:
            # If the user does not exist, raise an AuthenticationError
            logger.debug(f"User does not exists")
            raise AuthenticationError("User not found.")
        
        # Use Django's built-in check_password function to verify the password
        if not user.check_password(password):
            # If the password does not match, raise an AuthenticationError
            raise AuthorizationError()
        return True