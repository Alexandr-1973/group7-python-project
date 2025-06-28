from django.shortcuts import render, redirect, get_object_or_404
from .models import Event
from .forms import EventForm, RecurringEventForm
from django.contrib.auth.decorators import login_required
from datetime import timedelta

@login_required
def calendar_view(request):
    events = Event.objects.filter(user=request.user).order_by('date', 'time')
    return render(request, 'diary/calendar.html', {'events': events})

@login_required
def add_event(request):
    if request.method == 'POST':
        event_form = EventForm(request.POST)
        recurring_form = RecurringEventForm(request.POST)

        if event_form.is_valid():
            event = event_form.save(commit=False)
            event.user = request.user

            if event.is_recurring:
                if recurring_form.is_valid():
                    start = recurring_form.cleaned_data['recurrence_start']
                    end = recurring_form.cleaned_data['recurrence_end']

                    event.date = start
                    event.recurrence_start = start
                    event.recurrence_end = end
                    event.save()

                    current_date = start + timedelta(days=7)
                    while current_date <= end:
                        Event.objects.create(
                            title=event.title,
                            location=event.location,
                            date=current_date,
                            time=event.time,
                            is_recurring=True,
                            recurrence_start=start,
                            recurrence_end=end,
                            user=request.user,
                        )
                        current_date += timedelta(days=7)

                    return redirect('calendar:calendar_view')
                else:
                    return render(request, 'diary/add_event.html', {
                        'event_form': event_form,
                        'recurring_form': recurring_form
                    })

            else:
                event.save()
                return redirect('calendar:calendar_view')

    else:
        event_form = EventForm()
        recurring_form = RecurringEventForm()

    return render(request, 'diary/add_event.html', {
        'event_form': event_form,
        'recurring_form': recurring_form
    })

@login_required
def delete_event(request, pk):
    event = get_object_or_404(Event, pk=pk, user=request.user)
    if request.method == 'POST':
        event.delete()
        return redirect('calendar:calendar_view')
    return render(request, 'diary/event_confirm_delete.html', {'event': event})