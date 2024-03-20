from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from authuser.models import User

#Form used for reigstering a new user
class RegistrationForm(UserCreationForm):
    #Takes the following as parameters, includes validation and provides a help message on whats required
    email = forms.EmailField(required=True, help_text='Required. Enter a valid email address.')

    username = forms.CharField(max_length=30, required=True, help_text='Required. Enter a valid username.')
    #The widget is used to make the inputted text appear as dots to obscure the entry
    password1 = forms.CharField(widget=forms.PasswordInput, help_text='Required. Enter a secure password.')
    password2 = forms.CharField(widget=forms.PasswordInput, help_text='Required. Enter the same password again.')
    first_name = forms.CharField(max_length=30, required=True, help_text='Required. Enter your first name.')
    last_name = forms.CharField(max_length=30, required=True, help_text='Required. Enter your last name.')

    class Meta:
        #Makes use of the base User model
        model = User
        fields = ['email', 'username', 'password1', 'password2', 'first_name', 'last_name']


#Form used for logging in, similar to above
class LoginForm(forms.Form):
    #Takes an email and password as input, uses the same widget to obscure the sensitive input
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)