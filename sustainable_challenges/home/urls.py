from django.urls import path

from accounts.views import login_view
from . import views

app_name="home"
urlpatterns = [
    path("", views.index, name="index"),
    path("login/", login_view, name="login")
]