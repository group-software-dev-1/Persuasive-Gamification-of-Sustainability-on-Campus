from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate
from .forms import RegistrationForm, LoginForm  

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home:index')  
    else:
        form = RegistrationForm()

    return render(request, 'register.html', {'form': form, 'errors': form.errors})

def my_view(request):
    messages.success(request, 'This is a success message.')
    return render(request, 'my_template.html')


def login_view(request):  
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            print(f"Submitted data: {request.POST}")
            print(f"Cleaned data: {form.cleaned_data}")

            user = authenticate(request, email=email, password=password)

            if user is not None:
                login(request, user)
                print(f"Logged in user: {user}")
                return redirect('home:index')
            else:
                messages.error(request, 'Invalid email or password.')
        else:
            print(f"Form errors: {form.errors}")
            messages.error(request, 'Invalid form submission.')
    else:
        form = LoginForm()

    return render(request, 'home/login.html', {'form': form})



