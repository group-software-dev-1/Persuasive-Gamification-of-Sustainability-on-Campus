from django.urls import path
from .views import register, login_view

app_name = 'authuser'
urlpatterns = [
    path('', login_view, name='login'),
    path('register/', register, name="register")
]
