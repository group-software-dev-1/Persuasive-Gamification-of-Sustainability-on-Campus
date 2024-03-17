from django import forms
from .models import PlaceOfInterest

class PlaceOfInterestForm(forms.ModelForm):
    '''
    The Form for submitting a place of interest
    '''
    class Meta:
        model = PlaceOfInterest
        fields = ('title', 'desc','lat', 'lon')

        widgets = {
            'lat': forms.NumberInput(attrs={'id':'lat_id'}),
            'lon': forms.NumberInput(attrs={'id':'lon_id'}),
        }