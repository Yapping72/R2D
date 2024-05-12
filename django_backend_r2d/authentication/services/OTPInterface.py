from abc import ABC, abstractmethod

class OTPInterface(ABC):
    """OTP Interface that all OTP services must implement"""
    @abstractmethod
    def generate_otp(self, length: int) -> str:
        """Generate a random hashed OTP."""
        pass
    
    @abstractmethod
    def store_otp(self, otp:str) -> str:
        """Performs business logic i.e., hashing and storing of otp"""
    
    @abstractmethod
    def is_valid(self, otp_expiry) -> str:
        """Checks if OTP has expired """