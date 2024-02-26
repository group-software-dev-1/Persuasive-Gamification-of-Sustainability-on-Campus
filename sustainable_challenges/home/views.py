from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader



def index(request):
    return render(request, 'home/index.html', {"is_staff": request.user.is_staff,
                                               "is_authenticated": request.user.is_authenticated})

def login(request):
    return render(request, "home/login.html")