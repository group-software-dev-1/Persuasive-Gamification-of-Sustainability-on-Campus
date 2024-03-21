from django.urls import path
from . import views

app_name="forum"
urlpatterns = [
    path("forum/", views.forum, name="forum"),
    path("post/", views.post, name="post"),
    path("announce/", views.announce, name="announce"),
    path("forum/suggestion/<int:suggestion_id>", views.suggestion, name="suggestion"),
    path("forum/announcement/<int:announcement_id>", views.announcement, name="announcement"),
    path('forum/suggestion/delete_post/<int:id>', views.delete_post_function, name='delete_post'),
]