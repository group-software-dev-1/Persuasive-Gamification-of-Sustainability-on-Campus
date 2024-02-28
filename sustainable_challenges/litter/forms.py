from django import forms
from .models import LitterInstance

class InstanceForm(forms.ModelForm):
    '''
    The Form for reporting an instance of litter
    The only thing this form will really accept is the image
    Everything else for the LitterInstance model will come from either js or the report view
    '''
    class Meta:
        model = LitterInstance
        fields = ('img',)

        widgets = {
            'lat': forms.NumberInput(attrs={'hidden':'hidden'}),
            'lon': forms.NumberInput(attrs={'hidden':'hidden'}),
        }

class ApproveForm(forms.Form):
    '''
    Form for updating the status of an instance
    '''
    choices = ((1, 'Approve'), (2, 'Reject'))
    options = forms.ChoiceField(label='Options', choices=choices)

class TimeRangeForm(forms.Form):
    '''
    The form for selecting the date time range to display on the heatmap
    '''
    s_date = forms.DateTimeField(label='Start date', widget=forms.DateTimeInput(attrs={'type': 'date'}))
    e_date = forms.DateTimeField(label='End date', widget=forms.DateTimeInput(attrs={'type': 'date'}))