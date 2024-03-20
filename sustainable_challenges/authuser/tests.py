from django.test import TestCase
from authuser.forms import RegistrationForm, LoginForm
from authuser.models import User
from django.urls import reverse
from django.contrib.auth import get_user_model

class RegistrationFormTest(TestCase):

    def test_valid_registration_form(self):
        data = {
            'email': 'test@example.com',
            'username': 'testuser',
            'password1': 'securepassword123',
            'password2': 'securepassword123',
            'first_name': 'John',
            'last_name': 'Doe',
        }
        form = RegistrationForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_registration_form(self):
        data = {
            'email': 'invalidemail',
            'username': '',  # Required field
            'password1': 'password',
            'password2': 'differentpassword',
            'first_name': 'John',
            'last_name': 'Doe',
        }
        form = RegistrationForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)
        self.assertIn('username', form.errors)
        self.assertIn('password2', form.errors)

class LoginFormTest(TestCase):

    def test_valid_login_form(self):
        data = {
            'email': 'test@example.com',
            'password': 'securepassword123',
        }
        form = LoginForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_login_form(self):
        data = {
            'email': 'invalidemail',
            'password': '',  # Required field
        }
        form = LoginForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)
        self.assertIn('password', form.errors)

class UserModelTest(TestCase):

    def setUp(self):
        self.user_data = {
            'email': 'test@example.com',
            'username': 'testuser',
            'password': 'securepassword123',
            'first_name': 'John',
            'last_name': 'Doe',
            'points': 100,
            'is_active': True,
            'is_staff': False,
            'is_superuser': False,
            
        }

    def test_create_user(self):
        user = User.objects.create_user(**self.user_data)
        self.assertEqual(user.email, self.user_data['email'])
        self.assertEqual(user.username, self.user_data['username'])
        self.assertEqual(user.first_name, self.user_data['first_name'])
        self.assertEqual(user.last_name, self.user_data['last_name'])
        self.assertEqual(user.points, self.user_data['points'])
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_superuser)
        self.assertFalse(user.is_staff)
        self.assertIsNotNone(user.date_joined)

    def test_create_superuser(self):
        superuser = User.objects.create_superuser(**self.user_data)
    
        self.assertEqual(superuser.email, self.user_data['email'])
        self.assertEqual(superuser.username, self.user_data['username'])
        self.assertEqual(superuser.first_name, self.user_data['first_name'])
        self.assertEqual(superuser.last_name, self.user_data['last_name'])
        self.assertEqual(superuser.points, self.user_data['points'])
        self.assertTrue(superuser.is_active)
        self.assertTrue(superuser.is_superuser)
        self.assertTrue(superuser.is_staff)
        self.assertIsNotNone(superuser.date_joined)

    def test_get_full_name(self):
        user = User.objects.create_user(**self.user_data)
        self.assertEqual(user.get_full_name(), f"{self.user_data['first_name']} {self.user_data['last_name']}")

    def test_get_short_name(self):
        user = User.objects.create_user(**self.user_data)
        self.assertEqual(user.get_short_name(), self.user_data['first_name'])

    def test_user_string_representation(self):
        user = User.objects.create_user(**self.user_data)
        self.assertEqual(str(user), self.user_data['email'])

class AuthuserViewsTest(TestCase):
    def setUp(self):
        self.test_user = User.objects.create_user(username='testuser', password='testpassword', email='test@example.com')

    def test_register_view(self):
        response = self.client.get(reverse('authuser:register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')

        form_data = {
            'email': 'test1@example.com',
            'username': 'test1user',  
            'password1': 'testpassword',
            'password2': 'testpassword',
            'first_name': 'test',    
            'last_name': 'name',      
        }

        response = self.client.post(reverse('authuser:register'), form_data)
        self.assertRedirects(response, reverse('home:index'))
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_login_view(self):
        response = self.client.get(reverse('authuser:login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

        response = self.client.post(reverse('authuser:login'), {
            'email': 'test@example.com',
            'password': 'testpassword',
        })
        self.assertRedirects(response, reverse('home:index'))
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_logout_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('authuser:logout'))
        self.assertRedirects(response, reverse('home:index'))
        self.assertFalse(response.wsgi_request.user.is_authenticated)