from django import forms
from django.forms import ModelForm
from .models import LitterInstance

class InstanceForm(ModelForm):
    class Meta:
        model = LitterInstance
        fields = ('img',)

        widgets = {
            'lat': forms.NumberInput(attrs={'hidden':'hidden'}),
            'lon': forms.NumberInput(attrs={'hidden':'hidden'}),
        }

