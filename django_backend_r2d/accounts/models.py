from django.db import models
from django.contrib.auth.models import AbstractUser

"""
User class overrides django's default user to incorporate different roles.
"""
class User(AbstractUser):
    ROLE_CHOICES = [
        ('NORMAL_USER', 'Normal User'),
        ('PREMIUM_USER', 'Premium User'),
        ('IT_ADMINISTRATOR', 'IT Administrator'),
        ('ROOT','Root')
    ]
    
    role = models.CharField(
        max_length=50,
        choices=ROLE_CHOICES,
        default='NORMAL_USER',  # Set the default value here
    )
    
    # For security purposes we allow users to provide display names
    # Defaults to username if not provided

    preferred_name = models.CharField(max_length=255, blank=True, null=True) 
    
    def save(self, *args, **kwargs):
        if not self.preferred_name:
            self.preferred_name = self.username
        super().save(*args, **kwargs)

    def __str__(self):
        fields = {
            'username': self.username,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'preferred_name':self.preferred_name,
            'role': self.role,
            'is_active': self.is_active,
            'date_joined': self.date_joined.strftime('%Y-%m-%d %H:%M:%S') if self.date_joined else None,
            'last_login': self.last_login.strftime('%Y-%m-%d %H:%M:%S') if self.last_login else None,
        }
        return ', '.join(f"{key}: {value}" for key, value in fields.items() if value is not None)