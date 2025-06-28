"""
App configuration for the contacts app.
"""

from django.apps import AppConfig


class ContactsConfig(AppConfig):
    """Configuration for the contacts app."""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'contacts'
