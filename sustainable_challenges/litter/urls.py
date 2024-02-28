from django.urls import path

from . import views

app_name="litter"
urlpatterns = [
    path("latest/", views.latest, name="latest"),
    path("instance/<int:instance_id>/", views.instance, name="instance"),
    path("report/", views.report, name='report'),
    path("heatmap/", views.heatmap, name='heatmap'),
    path("your-instances/", views.your_instances, name="your instances"),
]