"""
Views for user authentication, profile management, and password reset.
"""

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from .forms import (
    RegisterForm,
    LoginForm,
    ProfileForm,
    ChangeUsernameForm,
    ChangeEmailForm,
)


def signup(request):
    """Handle user registration."""
    if request.user.is_authenticated:
        return redirect(to="contacts:contact_view")

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request, "Account successfully created! You can now log in."
            )
            return redirect("users:login")
            # return redirect(to="contacts:contact_view")
        else:
            return render(request, "users/signup.html", context={"form": form})

    return render(request, "users/signup.html", context={"form": RegisterForm()})


def loginuser(request):
    """Authenticate and log in a user."""
    if request.user.is_authenticated:
        return redirect(to="contacts:contact_view")

    if request.method == "POST":
        user = authenticate(
            username=request.POST["username"], password=request.POST["password"]
        )
        if user is None:
            messages.error(request, "Username or password didn't match")
            return redirect(to="users:login")

        login(request, user)
        return redirect(to="contacts:contact_view")

    return render(request, "users/login.html", context={"form": LoginForm()})


@login_required
def logoutuser(request):
    """Log out the current user."""
    logout(request)
    return redirect("base")
    # return redirect(to="contacts:contact_view")


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    """View for handling password reset requests."""
    template_name = "users/password_reset.html"
    email_template_name = "users/password_reset_email.html"
    html_email_template_name = "users/password_reset_email.html"
    success_url = reverse_lazy("users:password_reset_done")
    success_message = (
        "An email with instructions to reset your password has been sent to %(email)s."
    )
    subject_template_name = "users/password_reset_subject.txt"


@login_required
def profile(request):
    """Display and update user profile, password, username, and email."""
    profile_form = ProfileForm(instance=request.user.profile)
    change_password_form = PasswordChangeForm(request.user)
    change_username_form = ChangeUsernameForm()
    change_email_form = ChangeEmailForm()
    if request.method == "POST":
        if "avatar" in request.FILES:
            profile_form = ProfileForm(
                request.POST, request.FILES, instance=request.user.profile
            )
            if profile_form.is_valid():
                profile_form.save()
                messages.success(request, "Your profile is updated successfully")
                return redirect(to="users:profile")

        if "old_password" in request.POST:
            change_password_form = PasswordChangeForm(request.user, data=request.POST)
            if change_password_form.is_valid():
                change_password_form.save()
                messages.success(request, "Your password has been changed successfully")
                return redirect(to="users:login")

        if "username" in request.POST:
            change_username_form = ChangeUsernameForm(
                request.POST, instance=request.user
            )
            if (
                change_username_form.is_valid()
                and not User.objects.filter(username=request.POST["username"]).exists()
            ):
                change_username_form.save()
                messages.success(request, "Your username has been changed successfully")
                return redirect(to="users:profile")
            else:
                messages.error(request, "Username already exists")

        if "email" in request.POST:
            change_email_form = ChangeEmailForm(request.POST, instance=request.user)
            if (
                change_email_form.is_valid()
                and not User.objects.filter(email=request.POST["email"]).exists()
            ):
                change_email_form.save()
                messages.success(request, "Your email has been changed successfully")
                return redirect(to="users:profile")
            else:
                messages.error(request, "Email already exists")

    return render(
        request,
        "users/profile.html",
        {
            "profile_form": profile_form,
            "change_password_form": change_password_form,
            "change_username_form": change_username_form,
            "change_email_form": change_email_form,
        },
    )
