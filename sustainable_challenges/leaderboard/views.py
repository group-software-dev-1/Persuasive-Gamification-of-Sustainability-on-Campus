from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from authuser.models import User
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def leaderboard(request):
    users = User.objects.order_by("-level")[:100]
    return render(request, 'leaderboard.html', {"users": users,
                                                "is_staff": request.user.is_staff})