from django.test import TestCase
from game.models import *
from django.contrib.auth import get_user_model
from django.urls import reverse

class TestGame(TestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        """
        Sets up the system of testing
        """
        get_user_model().objects.create_user(email='user@email.com', password='notpassword', is_staff=False, username="user")

    def test_game_load(self):
        """
        Tests if page loads correctly when user logged in
        """
        self.client.login(email='user@email.com', password='notpassword')
        response = self.client.get(reverse("game:game"))
        self.assertEqual(response.status_code, 200)