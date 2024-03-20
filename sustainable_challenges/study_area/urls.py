# Study_Area/urls.py

from django.urls import path

from .views import home, event, create_event, event_detail, invalid_event, restricted_access 

urlpatterns = [
    path('', home, name='home'),
    path('event/', event, name='event'),
    path('create_event/', create_event, name='create_event'),
    path('event_details/<int:event_id>/', event_detail, name='event_detail'),
    path('invalid_event/', invalid_event, name='invalid_event'), 
    path('restricted_access/', restricted_access, name='restricted_access'), 
]
