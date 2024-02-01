from django.db import models
from django.contrib.auth.models import AbstractUser

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
        return self.username
