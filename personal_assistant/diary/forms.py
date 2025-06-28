from django import forms
from .models import Event


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'location', 'date', 'time', 'is_recurring']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
        }


class RecurringEventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['recurrence_start', 'recurrence_end']
        widgets = {
            'recurrence_start': forms.DateInput(attrs={'type': 'date'}),
            'recurrence_end': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start = cleaned_data.get('recurrence_start')
        end = cleaned_data.get('recurrence_end')
        if start and end and start > end:
            raise forms.ValidationError("End date must be after start date.")
        return cleaned_data
