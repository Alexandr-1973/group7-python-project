from django.db import models
from django.contrib.auth.models import User

class Event(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    location = models.CharField(max_length=200, blank=True)
    date = models.DateField()
    time = models.TimeField()
    is_recurring = models.BooleanField(default=False)
    recurrence_start = models.DateField(null=True, blank=True)
    recurrence_end = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.title} on {self.date} at {self.time}"