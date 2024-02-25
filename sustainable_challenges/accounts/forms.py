
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from accounts.models import Player  #

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text='Required. Enter a valid email address.')
    username = forms.CharField(max_length=30, required=True, help_text='Required. Enter a valid username.')
    password1 = forms.CharField(widget=forms.PasswordInput, help_text='Required. Enter a secure password.')
    password2 = forms.CharField(widget=forms.PasswordInput, help_text='Required. Enter the same password again.')
    first_name = forms.CharField(max_length=30, required=True, help_text='Required. Enter your first name.')
    last_name = forms.CharField(max_length=30, required=True, help_text='Required. Enter your last name.')

    class Meta:
        model = Player
        fields = ['email', 'username', 'password1', 'password2', 'first_name', 'last_name']



class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)