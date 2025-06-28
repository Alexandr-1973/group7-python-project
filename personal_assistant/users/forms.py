"""
Forms for user registration, authentication, and profile management.
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Profile


class RegisterForm(UserCreationForm):
    """Form for registering a new user."""

    username = forms.CharField(max_length=100, required=True)

    email = forms.EmailField(required=True)

    password1 = forms.CharField(
        min_length=4, max_length=20, required=True, widget=forms.PasswordInput()
    )
    password2 = forms.CharField(
        min_length=4, max_length=20, required=True, widget=forms.PasswordInput()
    )

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class LoginForm(AuthenticationForm):
    """Form for user login."""

    class Meta:
        model = User
        fields = ["username", "password"]


class ProfileForm(forms.ModelForm):
    """Form for updating user profile avatar."""

    avatar = forms.ImageField(widget=forms.FileInput(attrs={"style": "display: none;"}))

    class Meta:
        model = Profile
        fields = ['avatar']


class ChangePasswordForm(forms.Form):
    """Form for changing user password."""

    old_password = forms.CharField(
        min_length=4, max_length=20, required=True, widget=forms.PasswordInput()
    )
    password1 = forms.CharField(
        min_length=4, max_length=20, required=True, widget=forms.PasswordInput()
    )
    password2 = forms.CharField(
        min_length=4, max_length=20, required=True, widget=forms.PasswordInput()
    )

    class Meta:
        model = User
        fields = ["old_password", "password1", "password2"]


class ChangeUsernameForm(forms.ModelForm):
    """Form for changing username."""

    username = forms.CharField(max_length=100)

    class Meta:
        model = User
        fields = ["username"]


class ChangeEmailForm(forms.ModelForm):
    """Form for changing user email."""

    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["email"]