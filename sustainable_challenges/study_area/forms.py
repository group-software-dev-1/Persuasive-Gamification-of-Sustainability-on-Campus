from django import forms
from .models import Event

#Form used to create an event
#Takes parameters:
#Name - Name of the event
#Description - description of the event
#date_time - The start of the event, handeled using a basic calendar widget for ease of input, is a date time field
#duration - the length of the event and choices that the user can select from. saved as different form to whats inputted for datetime calculations elsewhere
#Points_worth - How much attending the event will award the user
#location - the location of the event
class EventForm(forms.ModelForm):
    name = forms.CharField(max_length=100)
    description = forms.CharField(widget=forms.Textarea)
    date_time = forms.DateTimeField(input_formats=['%Y-%m-%dT%H:%M'], required=False, widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'placeholder': 'YYYY-MM-DDThh:mm'}))
    duration = forms.ChoiceField(choices=[('0:30:00', '30 minutes'), ('1:00:00', '1 hour'), ('1:30:00', '1 hour 30 minutes'), ('2:00:00', '2 hours'), ('2:30:00', '2 hours 30 minutes'), ('3:00:00', '3 hours')], required=True)
    location = forms.CharField(max_length=100) 

    class Meta:
        model = Event
        fields = ['name', 'description', 'date_time', 'duration', 'location'] 
