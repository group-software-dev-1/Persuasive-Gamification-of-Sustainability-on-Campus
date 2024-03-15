from django.urls import path

from . import views

app_name="poi"
urlpatterns = [
    path("map/", views.latest, name="map"),
    path("info/<int:poi_id>/", views.instance, name="info"),
    path("submit/", views.report, name='submit'),
]