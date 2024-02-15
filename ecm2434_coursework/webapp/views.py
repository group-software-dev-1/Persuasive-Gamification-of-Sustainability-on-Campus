from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world. You're at the index. Maybe need to figure out how to have the site work without the /index in url")
