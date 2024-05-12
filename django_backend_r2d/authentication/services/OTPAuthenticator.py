from django.contrib.auth.models import User

from authentication.services.AuthenticationInterface import AuthenticationInterface
from authentication.services.AuthenticationExceptions import AuthenticationError
from authentication.services.OTPInterface import OTPInterface
from notification.services.EmailNotificationInterface import EmailNotificationInterface
from django.utils import timezone
from ..models import OTP
from ..models import FailedLoginAttempt

class OTPAuthenticator(AuthenticationInterface):
    """Performs OTP authentication"""
    def __init__(self, otp_service:OTPInterface, notification:EmailNotificationInterface):
        self.otp_service = otp_service
        self.notification = notification

    def register(self, user) -> str:
        """Generate an OTP, associate it with the user, and send it via email."""
        otp = self.otp_service.generate_otp(8)  # creates an 8-digit otp
        self.otp_service.store_otp(user, otp)
        self.notification.send_email(user.email, "Secure Login - method: OTP.", f"This is your OTP: {otp}. Please enter it within 3 minutes.")
        print(f"OTP: Your OTP is: {otp} Sent to {user.email}-- FROM OTPAuthenticator.py")
        return otp

    def authenticate(self, user_id:str, provided_otp:str) -> bool:
        """
        Verify the provided OTP for the user.
        After 5 failed attempts the account will be locked.
        """
        try:
            # Retrieve the stored OTP associated with the user
            stored_otp = OTP.objects.get(user_id=user_id)
            is_correct = self.otp_service.verify_otp(provided_otp, stored_otp.otp)
            is_valid = self.otp_service.is_valid(stored_otp.timestamp)
            
            try:
                stored_failedAttempt, created = FailedLoginAttempt.objects.get_or_create(user_id=user_id)
            except FailedLoginAttempt.DoesNotExist:
                # If row don't exist
                FailedLoginAttempt.objects.create(timestamp=timezone.now(), failed_count = 0, user_id = user_id)
            
            if is_correct is True and is_valid is True:
                # Reset failed count
                stored_failedAttempt.reset_failed_attempts()
                return True
            else:
                # Add failed count
                if stored_failedAttempt.check_timestamp():
                    stored_failedAttempt.reset_failed_attempts()
                    stored_failedAttempt.add_failed_attempt()
                else:
                    stored_failedAttempt.add_failed_attempt()
                return False
            
        except User.DoesNotExist:
            raise AuthenticationError("Oops your account doesn't seem to exists.")
        except OTP.DoesNotExist:
            raise AuthenticationError("No valid OTP found for user.")
