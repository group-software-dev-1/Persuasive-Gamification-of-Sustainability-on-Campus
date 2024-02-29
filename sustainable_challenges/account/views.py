# views.py
from django.http import HttpResponse
from django.shortcuts import render
from authuser.forms import RegistrationForm, LoginForm
from django.contrib.auth import login, logout, authenticate
import authuser.models


def user_account(request):
  user = request.user  # Retrieve the current logged-in user
  context = {
      'user': user,
      'is_staff': request.user.is_staff# Pass the user object to the template
  }
  return render(request, 'user_account.html', context)
  
def admin_account(request):
  if not request.user.is_staff:
      return HttpResponse("Unauthorized", status=401)
  return render(request, "admin_account.html", {'is_staff': request.user.is_staff})
