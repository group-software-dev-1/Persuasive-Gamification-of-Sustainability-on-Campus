from django.test import TestCase, Client
from django.urls import reverse
from game.models import Raffle
from authuser.forms import RegistrationForm
from authuser.models import User  

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
