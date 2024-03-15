from django.urls import path

from . import views

app_name="poi"
urlpatterns = [
    # path("map/", views.map, name="map"),
    path("info/<int:poi_id>/", views.information, name="info"),
    # path("submit/", views.submit, name='submit'),
]