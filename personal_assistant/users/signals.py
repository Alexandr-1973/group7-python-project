"""
Signals for user profile creation on user registration.
"""

from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver

from .models import Profile


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    """Create a Profile instance when a new User is created."""
    if created:
        profile = Profile.objects.create(user=instance)
        profile.save()