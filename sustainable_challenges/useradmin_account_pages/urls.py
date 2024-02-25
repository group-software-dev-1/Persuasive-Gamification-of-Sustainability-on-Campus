# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('user/account/', views.user_account, name='user_account'),
    path('admin/account/', views.admin_account, name='admin_account'),
    path('admin/account/', views.admin_account, name='admin_account'),
    path('approve-litter-instance/', views.approve_litter_instance, name='approve_litter_instance'),
]
