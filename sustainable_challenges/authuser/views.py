from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from authuser.forms import RegistrationForm, LoginForm  

#View that handles registration
def register(request):
    #Checks if request is a POST
    if request.method == 'POST':
        #If it is, creates a registration with the data in the post request
        form = RegistrationForm(data=request.POST)
        #If the form created is valid
        if form.is_valid():
            #saves the user in the database, and then logs them in
            user = form.save()
            login(request, user)
            #redirects them to the home page
            return redirect('home:index')  
    else:
        #If the request isnt post, created a form
        form = RegistrationForm()
    #and then render the registration form with the errors
    return render(request, 'register.html', {'form': form, 'errors': form.errors, 'is_staff': request.user.is_staff})

#Login view, quite similar to above
def login_view(request):
    #checks if post
    if request.method == 'POST':
        #creates a loginform with the data from post
        form = LoginForm(data=request.POST)
        #if the form is valid
        if form.is_valid():
            #get the cleaned data from the form
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            #Authenicates the user
            user = authenticate(request, email=email, password=password)
            #If the authentication was succesful
            if user is not None:
                #Logs the user in, then returns to home page
                login(request, user)
                print(f"Logged in user: {user}")
                return redirect('home:index')
            else:
                #If authentication fails, lets user know that its wrong
                messages.error(request, 'Invalid email or password.')
        else:
            #If form isnt valid, lets the us know
            print(f"Form errors: {form.errors}")
            messages.error(request, 'Invalid form submission.')
    else:
        #And if the request isnt a post
        form = LoginForm()
    #creates one and renders 
    return render(request, 'login.html', {'form': form, 'is_staff': request.user.is_staff})

#Logging out
def logout_view(request):
    #Puts info from request into logout
    logout(request)
    #Redirects back to home
    return redirect('home:index')