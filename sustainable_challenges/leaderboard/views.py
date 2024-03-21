from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from authuser.models import User

# Create your views here.

def leaderboard(request):
    users = User.objects.order_by("points")
    return render(request, 'leaderboard.html', {"users": users,
                                                "is_staff": request.user.is_staff})