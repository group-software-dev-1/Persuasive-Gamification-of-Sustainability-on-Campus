# models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
User = settings.AUTH_USER_MODEL

class CustomUser(AbstractUser):
    is_admin = models.BooleanField(default=False)

class LitterInstance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lat = models.DecimalField(default=0, decimal_places=7, max_digits=10)
    lon = models.DecimalField(default=0, decimal_places=7, max_digits=10)
    img = models.ImageField(null=True, blank=True, upload_to='images/litter/')
    datetime = models.DateTimeField("Date submitted")
    approved = models.BooleanField(default=False)

    def __str__(self):
        return f"User: {self.user}, {self.lat}, {self.lon} @ {self.datetime}"