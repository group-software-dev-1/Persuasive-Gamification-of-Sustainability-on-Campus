from django.contrib.auth.backends import ModelBackend
from .models import Player


class CustomEmailBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        try:
            user = Player.objects.get(email=email)
        except Player.DoesNotExist:
            return None

        if user.check_password(password):
            return user
        return None
