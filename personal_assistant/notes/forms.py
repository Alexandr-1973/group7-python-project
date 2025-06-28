"""
Forms for creating and editing notes and tags.
"""

from django.forms import ModelForm, CharField, TextInput

from .models import Tag, Note


class TagForm(ModelForm):
    """Form for creating a new tag."""

    name = CharField(min_length=3, max_length=25, required=True, widget=TextInput())

    class Meta:
        model = Tag
        fields = ['name']


class NoteForm(ModelForm):
    """Form for creating or editing a note."""

    name = CharField(min_length=5, max_length=50, required=True, widget=TextInput())
    description = CharField(min_length=10, max_length=150, required=True, widget=TextInput())

    class Meta:
        model = Note
        fields = ['name', 'description']
        exclude = ['tags']
