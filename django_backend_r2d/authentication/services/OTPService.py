from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone
from datetime import datetime, timedelta
import secrets

from authentication.services.OTPInterface import OTPInterface
from ..models import OTP

class OTPService(OTPInterface):
    def generate_otp(self, length:int = 8) -> str:
        """Creates an OTP (8 digit by default)"""
        return ''.join([str(secrets.randbelow(10)) for _ in range(length)])
    
    def _hash_otp(self, otp: str) -> str:
        """Hashes an OTP using django contrib auth hashers"""
        return make_password(otp)

    def verify_otp(self, provided_otp: str, hashed_otp: str) -> bool:
        """Determines if provided OTP is accurate"""
        return check_password(provided_otp, hashed_otp)

    def is_valid(self, timestamp, validity_period=10) -> bool:
        """
        Determines if provided OTP has not expired (10 minutes validity by default)
        Free-tier of email service is slow.
        """
        expiration_time = timestamp + timedelta(minutes=validity_period)
        return timezone.now() < expiration_time

    def store_otp(self, user, otp: str):
        """Hashes and associates the otp with the user object"""
        hashed_otp = self._hash_otp(otp)
        # Delete any existing OTP for the user
        OTP.objects.filter(user=user).delete()
        
        # Create a new OTP
        OTP.objects.create(user=user, otp=hashed_otp, timestamp=timezone.now())
        return hashed_otp


