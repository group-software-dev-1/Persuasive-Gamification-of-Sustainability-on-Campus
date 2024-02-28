# views.py
from django.shortcuts import render
from authuser.forms import RegistrationForm, LoginForm


def user_account(request):
    return render(request, "user_account.html")

def admin_account(request):
    if not request.user.is_staff:
        return HttpResponse("Unauthorized", status=401)
    return render(request, "admin_account.html")
