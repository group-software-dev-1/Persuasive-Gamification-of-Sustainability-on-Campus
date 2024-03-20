from datetime import timedelta
from .forms import EventForm
from django.test import TestCase, Client
from study_area.models import Event
from authuser.forms import RegistrationForm
from django.urls import reverse
from django.utils import timezone
from .models import Event
from sustainable_challenges.middleware import get_router_ip

class EventFormTestCase(TestCase):
    def test_event_form_valid(self):
        form_data = {
            'name': 'Test Event',
            'description': 'This is a test event',
            'date_time': '2024-03-20T10:00',
            'duration': '1:00:00',
            'location': 'Test Location'
        }
        form = EventForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_event_form_invalid(self):
        form_data = {
            'name': '',  # Empty name, should fail validation
            'description': 'This is a test event',
            'date_time': '2024-03-20T10:00',
            'duration': '1:00:00',
            'location': 'Test Location'
        }
        form = EventForm(data=form_data)
        self.assertFalse(form.is_valid())

class HomeViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_home_authenticated_non_staff(self):
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
        user = form.save()
        self.client.force_login(user)
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('home/index.html', response.templates[0].name)
        self.assertIn('home/base.html', response.templates[1].name)
        self.assertFalse(response.context['is_staff'])

    def test_home_authenticated_staff(self):
        user_data = {
            'email': 'staff@example.com',
            'username': 'staffuser',
            'password1': 'testpassword',
            'password2': 'testpassword',
            'first_name': 'Staff',
            'last_name': 'User',
        }
        form = RegistrationForm(user_data)
        self.assertTrue(form.is_valid())
        user = form.save()
        user.is_staff = True
        user.save()
        self.client.force_login(user)
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('home/index.html', response.templates[0].name)
        self.assertIn('home/base.html', response.templates[1].name)
        self.assertTrue(response.context['is_staff'])

class CreateEventViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        user_data = {
            'email': 'staff@example.com',
            'username': 'staffuser',
            'password1': 'testpassword',
            'password2': 'testpassword',
            'first_name': 'Staff',
            'last_name': 'User',
        }
        form = RegistrationForm(user_data)
        self.assertTrue(form.is_valid())
        self.staff_user = form.save()
        self.staff_user.is_staff = True
        self.staff_user.save()

    def test_render_create_event_form(self):
        self.client.force_login(self.staff_user)
        response = self.client.get('/study_area/create_event/')
        self.assertEqual(response.status_code, 200)

    def test_submit_event_form(self):
        self.client.force_login(self.staff_user)
        form_data = {
            'name': 'Test Event',
            'description': 'This is a test event.',
            'date_time': '2024-03-20T01:00',
            'duration': '1:00:00',
            'location': 'Test Location',
        }
        response = self.client.post('/study_area/create_event/', data=form_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/study_area/')
        event_exists = Event.objects.filter(name='Test Event').exists()
        self.assertTrue(event_exists)

class EventViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_event_view_rendering(self):
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
        user = form.save()
        self.client.force_login(user)
        response = self.client.get(reverse('event'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'study_area/event.html')

    def test_event_display_future(self):
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
        user = form.save()
        self.client.force_login(user)
        future_date = timezone.now() + timedelta(days=365)
        event = Event.objects.create(
            name='Test Event',
            description='This is a test event.',
            date_time=future_date,
            duration=timedelta(hours=1),
            location='Test Location'
        )
        response = self.client.get(reverse('event'))
        self.assertContains(response, 'Test Event')
        self.assertContains(response, 'This is a test event.')
        self.assertContains(response, 'Test Location')

    def test_event_display_past(self):
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
        user = form.save()
        self.client.force_login(user)
        past_date = timezone.now() - timedelta(days=365)
        event = Event.objects.create(
            name='Past Event',
            description='This is a past event.',
            date_time=past_date,
            duration=timedelta(hours=1),
            location='Past Location'
        )
        response = self.client.get(reverse('event'))
        self.assertNotContains(response, 'Past Event')
        self.assertNotContains(response, 'This is a past event.')
        self.assertNotContains(response, 'Past Location')

class OtherViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_invalid_event_view(self):
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
        user = form.save()
        self.client.force_login(user)
        response = self.client.get('/study_area/invalid_event/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'study_area/invalid_event.html')

    def test_restricted_access_view(self):
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
        user = form.save()
        self.client.force_login(user)
        response = self.client.get('/study_area/restricted_access/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'study_area/restricted_access.html')

class EventDetailViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_event_detail_view_open_event(self):
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
        user = form.save()
        self.client.force_login(user)
        event = Event.objects.create(
            name='Test Event',
            description='This is a test event.',
            date_time=timezone.now() - timedelta(hours=1),
            duration=timedelta(hours=2),
            location='Test Location',
            router_ip=get_router_ip(None)
        )
        url = reverse('event_detail', args=[event.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_event_detail_view_closed_event(self):
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
        user = form.save()
        self.client.force_login(user)
        event = Event.objects.create(
            name='Test Event',
            description='This is a test event.',
            date_time=timezone.now() - timedelta(days=1),
            duration=timedelta(hours=2),
            location='Test Location',
            router_ip=get_router_ip(None)
        )
        url = reverse('event_detail', args=[event.pk])
        response = self.client.get(url)
        self.assertRedirects(response, '/study_area/invalid_event/')

    def test_event_detail_view_closed_event_admin(self):
        user_data = {
            'email': 'staff@example.com',
            'username': 'staffuser',
            'password1': 'testpassword',
            'password2': 'testpassword',
            'first_name': 'Staff',
            'last_name': 'User',
        }
        form = RegistrationForm(user_data)
        self.assertTrue(form.is_valid())
        self.staff_user = form.save()
        self.staff_user.is_staff = True
        self.staff_user.save()
        self.client.force_login(self.staff_user)
        event = Event.objects.create(
            name='Test Event',
            description='This is a test event.',
            date_time=timezone.now() - timedelta(days=1),
            duration=timedelta(hours=2),
            location='Test Location',
            router_ip=get_router_ip(None)
        )
        url = reverse('event_detail', args=[event.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_event_detail_view_future_event(self):
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
        user = form.save()
        self.client.force_login(user)
        event = Event.objects.create(
            name='Test Future Event',
            description='This is a future event.',
            date_time=timezone.now() + timedelta(days=1),
            duration=timedelta(hours=2),
            location='Test Location',
            router_ip=get_router_ip(None)
        )
        url = reverse('event_detail', args=[event.pk])
        response = self.client.get(url)
        self.assertContains(response, '<p style="color: black;">Event hasn\'t started yet.</p>')

    def test_event_detail_register(self):
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
        user = form.save()
        self.client.force_login(user)
        event = Event.objects.create(
            name='Test Event',
            description='This is a test event.',
            date_time=timezone.now() - timedelta(hours=1),
            duration=timedelta(hours=2),
            location='Test Location',
            router_ip=get_router_ip(None)
        )
        url = reverse('event_detail', args=[event.pk])
        post_data = {
            'code': 'attend',
            'ip': event.router_ip
        }
        response = self.client.post(url, post_data)
        self.assertRedirects(response, '/study_area/event_details/1/')