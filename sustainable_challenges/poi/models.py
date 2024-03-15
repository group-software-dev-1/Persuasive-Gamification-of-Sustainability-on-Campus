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
    lat = models.DecimalField("Latitude", decimal_places=15, max_digits=18)
    lon = models.DecimalField("Longitude", decimal_places=15, max_digits=18)

    def __str__(self):
        return f"{self.lat}, {self.lon} | {self.desc}"