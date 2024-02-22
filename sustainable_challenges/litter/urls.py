from django.urls import path

from . import views

app_name="litter"
urlpatterns = [
    path("latest/", views.latest, name="latest"),
    path("instance/<int:instance_id>/", views.instance, name="instance"),
    path("report/", views.report, name='report'),
    path("heatmap/", views.heatmap, name='heatmap'),
    path("approve/<int:instance_id>/", views.approve, name="approve"),
]