# urls.py
from django.urls import path
from . import views
from django.contrib.auth.views import PasswordResetConfirmView
from django.urls import reverse_lazy

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    success_url = reverse_lazy('authuser:login')

app_name = "account"
# paths to app
urlpatterns = [
    path("user_account", views.user_account, name='user_account'),
    path("admin_account", views.admin_account, name='admin_account'),
    path("reset_email/", views.reset_email, name='reset_email'),
    path('reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/<uidb64>/<token>/complete/', views.password_reset_complete, name='password_reset_complete'),
]

