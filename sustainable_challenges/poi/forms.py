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

class LocationForm(forms.Form):
    '''
    The form for getting the users location when they try to visit a place
    '''
    lat = forms.DecimalField(widget=forms.NumberInput(attrs={'id':'lat_id', 'hidden': 'hidden'}), label="")
    lon = forms.DecimalField(widget=forms.NumberInput(attrs={'id':'lon_id', 'hidden': 'hidden'}), label="")
    acc = forms.DecimalField(widget=forms.NumberInput(attrs={'id':'acc_id', 'hidden': 'hidden'}), label="")