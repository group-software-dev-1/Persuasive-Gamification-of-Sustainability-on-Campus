from django.contrib import admin
from .models import Event

#Registers the event model to the database for developer uses
@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'date_time', 'router_ip')
    list_display_links = ('id', 'name')
