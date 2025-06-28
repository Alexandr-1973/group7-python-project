from django.urls import path
from . import views

app_name = 'calendar'

urlpatterns = [
    path('', views.calendar_view, name='calendar_view'),
    path('add/', views.add_event, name='add_event'),
    path('delete/<int:pk>/', views.delete_event, name='delete_event'),
]