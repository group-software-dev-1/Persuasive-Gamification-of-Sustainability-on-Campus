from django.db import models
from django.conf import settings
from django.utils import timezone

User = settings.AUTH_USER_MODEL

class Post(models.Model):
    '''
    Database model for Superclass Post

    Fields
    ------
    post_name: string
         Title of the post
    post_text: string
         The text of the post 
    poster: user
         The user who posted the post
    post_date: DateTime
              The Date and Time that this post was made
    '''
    post_name = models.CharField("Post Name", max_length=100)
    post_text = models.CharField("Post Text", max_length=400)
    poster = models.ForeignKey(User, on_delete=models.CASCADE, default=None, verbose_name="Poster")
    post_date = models.DateTimeField("Date Posted", default=timezone.now)
    class Meta:
        abstract = True

    def get_post_name(self):
        return self.post_name
    
    def get_post_text(self):
        return self.post_text

class Annoucement(Post):
    '''
    Database model for Subclass Announcement

    Fields
    ------
    post_name: string
         Title of the post
    post_text: string
         The text of the post 
    poster: user
         The user who posted the post
    post_date: DateTime
          The Date and Time that this post was made
    active: Boolean
          If the announcement is currently active
    '''
    active = models.BooleanField("Is Active", default=True)

class Suggestion(Post):
    '''
    Database model for Subclass Suggestion

    Fields
    ------
    post_name: string
         Title of the post
    post_text: string
         The text of the post 
    poster: user
         The user who posted the post
    post_date: DateTime
         The Date and Time that this post was made
    linked_announced: Announcement
         If the suggestion is attached to an announcement 
    '''
    linked_announced = models.ForeignKey( Annoucement, default=None, blank=True, null=True, on_delete=models.CASCADE, verbose_name="Announcement")
    def noEndorsements(self):
        return len(self.endorsements)

class Comment(models.Model):
    '''
    Database model for Subclass Suggestion

    Fields
    ------
    comment_text: string
         The text of the comment 
    poster: user
         The user who posted the post
    post_date: DateTime
          The Date and Time that this post was made
    linked_post = Suggestion
          The suggestion the comment is on
    linked_announcement = Announcement
          The announcement the comment is on
    '''
    comment_text = models.CharField("Comment Text", max_length= 400)
    linked_post = models.ForeignKey(Suggestion, default=None, blank=True, null=True, on_delete=models.CASCADE, verbose_name="Suggestion")
    linked_announcement = models.ForeignKey(Annoucement, default=None, blank=True, null=True, on_delete=models.CASCADE, verbose_name="Announcement")
    poster = models.ForeignKey(User, default=None, blank=True, null=True, on_delete=models.CASCADE, verbose_name="Poster")
    post_date = models.DateTimeField("Date Posted", default=timezone.now)

# Create your models here.
