"""
Forms for creating and editing contacts.
"""

from django.forms import ModelForm, CharField, EmailField, TextInput, DateField, DateInput
from phonenumber_field.formfields import PhoneNumberField
from .models import Contact


class ContactForm(ModelForm):
    """Form for creating or editing a contact."""
    first_name = CharField(
        min_length=2,
        max_length=150,
        required=True,
    )
    last_name = CharField(
        min_length=2,
        max_length=150,
        required=True,
    )
    address = CharField(
        max_length=150,
        required=False,
    )
    email = EmailField(
        max_length=150,
        required=True,
    )
    phone_number = PhoneNumberField(
        required=True,
        widget=TextInput(attrs={'placeholder': '+380xxxxxxxxx'})
    )
    birthday = DateField(
        required=False,
        widget=DateInput(attrs={'placeholder': 'YYYY-MM-DD'}),
        input_formats=['%Y-%m-%d']
    )

    class Meta:
        model = Contact
        fields = ['first_name', 'last_name', 'address', 'email', 'phone_number', 'birthday']