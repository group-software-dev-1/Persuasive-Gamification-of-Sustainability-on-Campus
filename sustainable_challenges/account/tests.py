from django.test import TestCase
from django.urls import reverse
from authuser.models import User
from django.core import mail

class AccountAppTests(TestCase):
    
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')
        
    def test_user_account_view(self):
        # Test user account view
        self.client.force_login(self.user)
        response = self.client.get(reverse('account:user_account'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user_account.html')
        self.assertContains(response, 'User Account Page')
        self.assertContains(response, 'Welcome, testuser!')
        self.assertContains(response, 'Email: test@example.com')
        
    def test_admin_account_view(self):
        # Test admin account view
        self.client.force_login(self.user)
        response = self.client.get(reverse('account:admin_account'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin_account.html')
        self.assertContains(response, 'Admin Account Page')
        self.assertContains(response, 'Welcome, testuser!')
        self.assertContains(response, 'Email: test@example.com')
        
    def test_reset_email_view(self):
        # Test reset email view
        self.client.login(email='test@example.com', password='testpassword')
        response = self.client.get(reverse('account:reset_email'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reset_email_form.html')
        
        # Test sending reset email
        response = self.client.post(reverse('account:reset_email'), {'email': 'test@example.com'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Password Reset Request')
        self.assertEqual(mail.outbox[0].to[0], 'test@example.com')
        self.assertIn('Password reset email sent successfully!', response.content.decode())
        
    def test_password_reset_complete_view(self):
        # Test password reset complete view
        response = self.client.get(reverse('account:password_reset_complete', kwargs={'uidb64': 'uidb64', 'token': 'token'}))
        self.assertEqual(response.status_code, 302)
