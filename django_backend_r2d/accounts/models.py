from django.db import models
from django.contrib.auth.models import AbstractUser

"""
User class overrides django's default user to incorporate different roles.
"""
class User(AbstractUser):
    ROLE_CHOICES = [
        ('NORMAL_USER', 'Normal User'),
        ('PAID_USER', 'Paid User'),
        ('IT_ADMINISTRATOR', 'IT Administrator'),
    ]
    
    role = models.CharField(
        max_length=50,
        choices=ROLE_CHOICES,
        default='NORMAL_USER',  # Set the default value here
    )

    def __str__(self):
        fields = {
            'username': self.username,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'role': self.role,
            'is_active': self.is_active,
            'is_staff': self.is_staff,
            'is_superuser': self.is_superuser,
            'date_joined': self.date_joined.strftime('%Y-%m-%d %H:%M:%S') if self.date_joined else None,
            'last_login': self.last_login.strftime('%Y-%m-%d %H:%M:%S') if self.last_login else None,
        }
        return ', '.join(f"{key}: {value}" for key, value in fields.items() if value is not None)