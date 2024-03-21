from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from forum.models import User, Suggestion, Annoucement, Comment
from django.urls import reverse

class TestLeaderboard(TestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        get_user_model().objects.create_user(email='is_staff@email.com', password='testPassword', is_staff=True, username="test")
        get_user_model().objects.create_user(email='not_staff@email.com', password='testPassword', is_staff=False, username="test2")
        
    def test_access_for_staff(self):
        self.client.login(email='is_staff@email.com', password='testPassword')
        response = self.client.get(reverse("leaderboard:leaderboard"))
        self.assertEqual(response.status_code, 200)

    def test_access_for_non_staff(self):
        self.client.login(email='not_staff@email.com', password='testPassword')
        response = self.client.get(reverse("leaderboard:leaderboard"))
        self.assertEqual(response.status_code, 200)

    def test_staff_gets_1_suggestion(self):
        self.client.login(email='is_staff@email.com', password='testPassword')
        response = self.client.get(reverse("leaderboard:leaderboard"))
        self.assertEqual(len(response.context['users']), 2)