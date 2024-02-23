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
