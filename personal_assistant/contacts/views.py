"""
Views for managing contacts, including creation, editing, and deletion.
"""

from django.shortcuts import render, redirect, get_object_or_404
from .forms import ContactForm
from .models import Contact
from datetime import datetime
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def contacts_view(request):
    """Display a list of contacts, with search and upcoming birthdays filtering."""
    query = request.GET.get("q", "")
    days_str = request.GET.get("days")

    contacts = Contact.objects.filter(user=request.user)

    if query:
        contacts = contacts.filter(first_name__icontains=query)

    if days_str and days_str.isdigit():
        days = int(days_str)
        today = datetime.today().date()
        upcoming_birthdays_list = []

        for contact in contacts:
            if contact.birthday:
                birthday_this_year = contact.birthday.replace(year=today.year)
                # birthday_this_year = datetime.strptime(contact.birthday, "%Y-%m-%d").date().replace(year=today.year)
                if birthday_this_year < today:
                    birthday_this_year = birthday_this_year.replace(year=today.year + 1)
                if 0 <= (birthday_this_year - today).days <= days:
                    upcoming_birthdays_list.append(contact)

        contacts = upcoming_birthdays_list

    return render(request, "contacts/contacts.html", {"contacts": contacts})


@login_required
def create_contact(request):
    """Create a new contact for the user."""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save(commit=False)
            contact.user = request.user
            contact.save()
            return redirect('contacts:contact_view')
    else:
        form = ContactForm()
    return render(request, 'contacts/create_contact.html', {'form': form})


@login_required
def edit_contact(request, contact_id):
    """Edit an existing contact for the user."""
    contact = get_object_or_404(Contact, id=contact_id, user=request.user)

    if request.method == 'POST':
        form = ContactForm(request.POST, instance=contact)
        if form.is_valid():
            form.save()
            return redirect('contacts:contact_view')
    else:
        form = ContactForm(instance=contact)
    return render(request, 'contacts/edit_contact.html', {'form': form})


@login_required
def delete_contact(request, contact_id):
    """Delete a contact for the user after confirmation."""
    contact = get_object_or_404(Contact, id=contact_id, user=request.user)
    if request.method == 'POST':
        contact.delete()
        return redirect('contacts:contact_view')
    return render(request, 'contacts/confirm_delete.html', {'contact': contact})