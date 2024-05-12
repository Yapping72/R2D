# Create your models here.
from django.db import models
from django.utils import timezone
from datetime import timedelta

from django.contrib.auth import get_user_model
User = get_user_model()
    
class OTP(models.Model):
    """Used to store OTP codes"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=128) # stores a hashed OTP
    timestamp = models.DateTimeField(auto_now_add=True)

class FailedLoginAttempt(models.Model):
    """Used to store OTP attempts"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    failed_count = models.PositiveIntegerField(default=0)

    def lock_account(self):
        if self.failed_count >= 5:
            self.user.is_active = False
            self.user.save()

    def add_failed_attempt(self):
        self.failed_count += 1
        if self.failed_count >= 5:
            self.lock_account()
        self.timestamp = timezone.now()
        self.save()
    
    def reset_failed_attempts(self):
        self.failed_count = 0
        self.timestamp = timezone.now()
        self.save()
        
    def check_timestamp(self):
        time_difference = timezone.now() - self.timestamp
        one_minute = timedelta(minutes=1)
        if time_difference > one_minute:
            # Time difference is greater than 1 minute
            return True
        else:
            # Time difference is less than or equal to 1 minute
            return False

    