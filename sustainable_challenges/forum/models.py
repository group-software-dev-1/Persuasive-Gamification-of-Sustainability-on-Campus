from django.db import models
from django.conf import settings
from django.utils import timezone
User = settings.AUTH_USER_MODEL

class Post(models.Model):
    post_name = models.CharField(max_length=100)
    post_text = models.CharField(max_length=400)
    poster = models.ForeignKey(User, default=None, blank=True, null=True, on_delete=models.CASCADE)
    post_date = models.DateTimeField(default=timezone.now)
    class Meta:
        abstract = True

    def get_post_name(self):
        return self.post_name
    
    def get_post_text(self):
        return self.post_text

class Annoucement(Post):
    active = models.BooleanField(default=True)

class Suggestion(Post):
    linked_announced = models.ForeignKey(Annoucement, default=None, blank=True, null=True, on_delete=models.CASCADE)
    endorsements = models.IntegerField(default=0)

class Comment(models.Model):
    comment_text = models.CharField(max_length= 400)
    linked_post = models.ForeignKey(Suggestion or Annoucement, on_delete=models.CASCADE)
    endorsements = models.IntegerField(default=0)
    poster = models.ForeignKey(User, default=None, blank=True, null=True, on_delete=models.CASCADE)
    post_date = models.DateTimeField(default=timezone.now)

# Create your models here.
