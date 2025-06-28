"""
Models for storing contact information.
"""

from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import User


class Contact(models.Model):
    """Model representing a user's contact."""
    first_name = models.CharField(max_length=150, null=False)
    last_name = models.CharField(max_length=150, null=False)
    address = models.CharField(max_length=150)
    email = models.EmailField(max_length=150, unique=True)
    phone_number = PhoneNumberField(unique=True)
    birthday = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

