from django.test import TestCase, Client
from game.models import *
from django.contrib.auth import get_user_model
from django.urls import reverse
from game.models import Raffle
from authuser.forms import RegistrationForm
from authuser.models import User  

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

    def test_game_non_logged_in(self):
        """
        Tests when a non logged in user tries to access the page
        """
        try:
            self.client.get(reverse("game:game"))
        except:
            self.assertTrue(True)

    def test_game_context(self):
        """
        Tests the context returned from the game
        """
        self.client.login(email='user@email.com', password='notpassword')
        response = self.client.get(reverse("game:game"))
        expected_current = {'name':'litter', 'tasks':1, 'points':100, 'number':1}
        self.assertEqual(expected_current, response.context[0]['current_context'])
        self.assertEqual(9, len(response.context[0]['level_contexts']))

class TestShop(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        """
        Sets up the system of testing
        """
        get_user_model().objects.create_user(email='user@email.com', password='notpassword', is_staff=False, username="user")

    def test_shop_load(self):
        """
        Tests if page loads correctly when user logged in
        """
        self.client.login(email='user@email.com', password='notpassword')
        response = self.client.get(reverse("game:shop"))
        self.assertEqual(response.status_code, 200)

    def test_shop_non_logged_in(self):
        """
        Tests when a non logged in user tries to access the page
        """
        try:
            self.client.get(reverse("game:shop"))
        except:
            self.assertTrue(True)

    def test_shop_context(self):
        """
        Tests the context returned from the game
        """
        self.client.login(email='user@email.com', password='notpassword')
        response = self.client.get(reverse("game:shop"))
        self.assertFalse(response.context[0]['response'])
        self.assertFalse(response.context[0]['success'])
        self.assertEqual(0, response.context[0]['points'])
        self.assertEqual({'amazon': 10000, 'john_lewis':10000, 'blackwells':50000, 'ram':50000, 'student_guild':50000, 'marketplace':50000}, response.context[0]['prize_to_points'])
        self.assertEqual(6, len(response.context[0]['completion']))

class RaffleViewTestCase(TestCase):

    def setUp(self):
        user_data = {
            'email': 'user@example.com',
            'username': 'regularuser',
            'password1': 'testpassword',
            'password2': 'testpassword',
            'first_name': 'Regular',
            'last_name': 'User',
        }
        form = RegistrationForm(user_data)
        self.assertTrue(form.is_valid())
        self.user = form.save()

        self.daily_raffle = Raffle.objects.create(name='Daily', num_participants=0, points_accumulated=0)
        self.weekly_raffle = Raffle.objects.create(name='Weekly', num_participants=0, points_accumulated=0)
        self.client = Client()

    def test_raffle_view_loads_correctly(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('game:raffle'))
        self.assertEqual(response.status_code, 200)

    def test_enter_daily_raffle(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('game:raffle'), {'code': 'daily', 'username': self.user.username})
        self.assertRedirects(response, reverse('game:raffle'))
        self.daily_raffle.refresh_from_db()
        self.assertIn(self.user.username, self.daily_raffle.participants.split(','))

    def test_enter_weekly_raffle(self):
        self.client.force_login(self.user)
        self.user.points += 500
        self.user.save()
        response = self.client.post(reverse('game:raffle'), {'code': 'weekly', 'username': self.user.username})
        self.assertRedirects(response, reverse('game:raffle'))
        self.weekly_raffle.refresh_from_db()
        self.assertIn(self.user.username, self.weekly_raffle.participants.split(','))

    def test_enter_weekly_raffle_no_points(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('game:raffle'), {'code': 'weekly', 'username': self.user.username})
        self.assertRedirects(response, reverse('game:raffle'))
        self.weekly_raffle.refresh_from_db()
        self.assertNotIn(self.user.username, self.weekly_raffle.participants.split(','))