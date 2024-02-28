from django.db import models
from django.conf import settings
User = settings.AUTH_USER_MODEL

class LitterInstance(models.Model):
    '''
    Database model for storing an instance of litter

    Fields
    ------
    user: Django user
          The user who reported this instance of litter
    lat: float
         The latitude of the reports location
    lon: float
         The longitude of the reports location
    img: string
         Path to the image of litter for this instance
    datetime: DateTime
              The Date and Time that this instance was reported
    approved: int
              The status of the report
              0 - pending approval,
              1 - approved,
              2 - rejected,
    '''
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="User")
    lat = models.DecimalField("Latitude", default=0, decimal_places=7, max_digits=10)
    lon = models.DecimalField("Longitude", default=0, decimal_places=7, max_digits=10)
    img = models.ImageField("Image", null=True, blank=True, upload_to='images/litter/')
    datetime = models.DateTimeField("Date submitted")
    approved = models.IntegerField("Approval status", default=0)

    def __str__(self):
        return f"User: {self.user}, {self.lat}, {self.lon} @ {self.datetime}"