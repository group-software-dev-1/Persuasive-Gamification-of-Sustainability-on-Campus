# views.py
from django.shortcuts import render
from django.core.mail import send_mail
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from authuser.forms import RegistrationForm, LoginForm
from django.contrib.auth import login, logout, authenticate
import authuser.models

from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model


def user_account(request):
    user = request.user  # Retrieve the current logged-in user
    context = {
        'user': user,  # Pass the user object to the template
    }
    return render(request, 'user_account.html', context)

def admin_account(request):
    #if not request.user.is_staff:
          # return HttpResponse("Unauthorized", status=401)
    
    user = request.user  # Retrieve the current logged-in user
    context = {
        'user': user,  # Pass the user object to the template
    }
    return render(request, 'admin_account.html', context)

def reset_email(request):
    if request.method == "POST":
        email = request.POST.get('email')
        User = get_user_model()
        
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return HttpResponse("Email address not found.")

        if user.is_authenticated:
            # Generate password reset token
            token = default_token_generator.make_token(user)

            # Construct password reset URL
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            reset_url = reverse('account:password_reset_confirm', kwargs={'uidb64': uidb64, 'token': token})
            reset_url = request.build_absolute_uri(reset_url)

            # Send email with reset link
            subject = 'Password Reset Request'
            message = reset_url
            send_mail(subject, message, 'Group.Software.Dev.Help@gmail.com', [user.email])

            return HttpResponse("Password reset email sent successfully!")
        else:
            # Handle the case where the user is not logged in
            # Redirect or render a form for password reset
            # For simplicity, let's just redirect to the login page
            return redirect('authuser:login')
    else:
        return render(request, 'reset_email_form.html')
    

def password_reset_complete(request, uidb64, token):
    # Redirect to the account page
    return redirect('authuser:login')
