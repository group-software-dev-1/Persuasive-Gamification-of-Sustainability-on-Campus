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
    desc = models.TextField("Description", default="")
    lat = models.DecimalField("Latitude", default=0, decimal_places=7, max_digits=10)
    lon = models.DecimalField("Longitude", default=0, decimal_places=7, max_digits=10)

    def __str__(self):
        return f"{self.lat}, {self.lon} | {self.desc}"