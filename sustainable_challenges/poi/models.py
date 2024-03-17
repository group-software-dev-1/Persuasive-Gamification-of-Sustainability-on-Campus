from django.db import models
from django.conf import settings
User = settings.AUTH_USER_MODEL

class PlaceOfInterest(models.Model):
    '''
    Database model for storing an instance of litter

    Fields
    ------
    desc: string
          Description and information about the place of interest
    lat: float
         The latitude of the reports location
    lon: float
         The longitude of the reports location
    '''
    title = models.CharField("Title", max_length=100)
    desc = models.TextField("Description")
    lat = models.DecimalField("Latitude", decimal_places=16, max_digits=19)
    lon = models.DecimalField("Longitude", decimal_places=16, max_digits=19)

    def __str__(self):
        return f"{self.lat}, {self.lon} | {self.desc}"
    

class VisitedPlaceOfInterest(models.Model):
    '''
     Database table to keep track of what users have visited where
     so that a user cannot vist the same place twice and get points for it again.
    
     Fields
     ------
     user: Django user
          The user that has visted the palce
     place: PlaceOfInterest
            The place that has been visited
    '''
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="User")
    place = models.ForeignKey(PlaceOfInterest, on_delete=models.CASCADE, verbose_name="Place Of Interest")

    def __str__(self):
        return f"{self.user} @ {self.place}"