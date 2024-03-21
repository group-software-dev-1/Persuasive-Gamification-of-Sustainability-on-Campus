from django.urls import path

from authuser.views import login_view
from . import views

app_name="home"
urlpatterns = [
    path("", views.index, name="index"),
    path("goals/", views.goals, name="goals"),
    path("privacy/", views.privacy, name="privacy")
]