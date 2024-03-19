from django.db import models
from datetime import timedelta

#Our event model
#name - the name
#description - the description
#date_time - time the event is occuring
#duration - the duration of the event
#points_worth - the points the event is worth
#router_ip - the ip of the internet access point at the event, can be updated by admins if it renews
#location - location of the event
#attendees - the username of the people that attend the event

class Event(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    date_time = models.DateTimeField(null=True)  # Allow null values
    duration = models.DurationField(default=timedelta(hours=1))  # Default duration is 1 hour
    points_worth = models.IntegerField(default=0)  # Default points worth is 0
    router_ip = models.CharField(max_length=50)
    location = models.CharField(max_length=100, default="")
    attendees = models.TextField(blank=True)  # Comma-separated list of attendees

    def __str__(self):
        return self.name
