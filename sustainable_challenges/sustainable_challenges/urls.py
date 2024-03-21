"""
URL configuration for sustainable_challenges project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

app_name = 'sustainable_challenges'

urlpatterns = [
    path('litter/', include('litter.urls')),
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('login/', include('authuser.urls')),
    path('game/', include('game.urls')),
    path('account/', include('account.urls')),
    path('study_area/', include('study_area.urls')),
    path('forum/', include('forum.urls')),
    path('poi/', include('poi.urls')),
    path('leaderboard/', include('leaderboard.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)