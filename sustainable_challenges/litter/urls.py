from django.urls import path

from . import views

app_name="litter"
urlpatterns = [
    path("latest/", views.LatestView.as_view(), name="latest"),
    path("instance/<int:instance_id>/", views.instance, name="instance"),
    path("report/", views.report, name='report'),
]