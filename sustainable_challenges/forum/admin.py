from django.contrib import admin

# Register your models here.
from forum.models import Annoucement, Suggestion, Comment
admin.site.register(Annoucement)
admin.site.register(Suggestion)
admin.site.register(Comment)