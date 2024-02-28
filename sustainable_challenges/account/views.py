# views.py
from django.shortcuts import render


def user_account(request):
    return render(request, "user_account.html")

def admin_account(request):
    if not request.user.is_admin:
        return HttpResponse("Unauthorized", status=401)
    return render(request, "admin_account")
