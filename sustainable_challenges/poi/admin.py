from django.contrib import admin
from .models import PlaceOfInterest, VisitedPlaceOfInterest

# Register your models here.
admin.site.register(PlaceOfInterest)
admin.site.register(VisitedPlaceOfInterest)