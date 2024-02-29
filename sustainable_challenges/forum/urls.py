from django.urls import path
from . import views

app_name="forum"
urlpatterns = [
    path("forum/", views.forum, name="forum"),
    path("post/", views.post, name="post"),
    path("forum/<int:suggestion_id>", views.suggestion, name="suggestion"),
    path("forum/annoucement/<int:announcement_id>", views.announcement, name="announcement")
]