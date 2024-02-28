# views.py
from django.http import HttpResponse
from django.shortcuts import render


def user_account(request):
    return render(request, "user_account.html", {'is_staff': request.user.is_staff})

def admin_account(request):
    if not request.user.is_staff:
        return HttpResponse("Unauthorized", status=401)
    return render(request, "admin_account.html", {'is_staff': request.user.is_staff})
