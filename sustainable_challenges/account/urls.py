# urls.py
from django.urls import path
from . import views

app_name = "account"
# paths to app
urlpatterns = [
    path("user_account", views.user_account, name='user_account'),
    path("admin_account", views.admin_account, name='admin_account'),
]
