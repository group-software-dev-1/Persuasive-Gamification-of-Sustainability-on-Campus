from django import forms
from .models import LitterInstance

class InstanceForm(forms.ModelForm):
    class Meta:
        model = LitterInstance
        fields = ('img',)

        widgets = {
            'lat': forms.NumberInput(attrs={'hidden':'hidden'}),
            'lon': forms.NumberInput(attrs={'hidden':'hidden'}),
        }

class ApproveForm(forms.Form):
    choices = ((1, 'Approve'), (2, 'Reject'))
    options = forms.ChoiceField(label='Options', choices=choices)

class TimeRangeForm(forms.Form):
    s_date = forms.DateTimeField(label='Start date', widget=forms.DateTimeInput(attrs={'type': 'date'}))
    e_date = forms.DateTimeField(label='End date', widget=forms.DateTimeInput(attrs={'type': 'date'}))