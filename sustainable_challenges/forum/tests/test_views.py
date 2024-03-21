from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from forum.models import User, Suggestion, Annoucement, Comment
from django.urls import reverse

class TestForum(TestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        get_user_model().objects.create_user(email='is_staff@email.com', password='testPassword', is_staff=True, username="test")
        get_user_model().objects.create_user(email='not_staff@email.com', password='testPassword', is_staff=False, username="test2")
        Suggestion.objects.create(poster=get_user_model().objects.get(pk=1),
                                  post_name='stest',
                                  post_text = 'stxt',
                                  post_date=timezone.now())
        Comment.objects.create(poster=get_user_model().objects.get(pk=1),
                                  comment_text = 'ctxt',
                                  post_date=timezone.now(),
                                  linked_announcement=None,
                                  linked_post=Suggestion.objects.get(id=1))
        Annoucement.objects.create(poster=get_user_model().objects.get(pk=1),
                                  post_name='atest',
                                  post_text='atxt',
                                  post_date=timezone.now(),
                                  active=True)
        
    def test_access_for_staff(self):
        self.client.login(email='is_staff@email.com', password='testPassword')
        response = self.client.get(reverse("forum:forum"))
        self.assertEqual(response.status_code, 200)

    def test_access_for_non_staff(self):
        self.client.login(email='not_staff@email.com', password='testPassword')
        response = self.client.get(reverse("forum:forum"))
        self.assertEqual(response.status_code, 200)
    
    def test_staff_gets_1_suggestion(self):
        self.client.login(email='is_staff@email.com', password='testPassword')
        response = self.client.get(reverse("forum:forum"))
        self.assertEqual(len(response.context['announcements']), 1)

    def test_staff_gets_1_announcement(self):
        self.client.login(email='is_staff@email.com', password='testPassword')
        response = self.client.get(reverse("forum:forum"))
        self.assertEqual(len(response.context['suggestions']), 1)

class TestPost(TestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        get_user_model().objects.create_user(email='is_staff@email.com', password='testPassword', is_staff=True, username="test")
        get_user_model().objects.create_user(email='not_staff@email.com', password='testPassword', is_staff=False, username="test2")

    def test_access_for_staff(self):
        self.client.login(email='is_staff@email.com', password='testPassword')
        response = self.client.get(reverse("forum:post"))
        self.assertEqual(response.status_code, 200)

    def test_access_for_non_staff(self):
        self.client.login(email='not_staff@email.com', password='testPassword')
        response = self.client.get(reverse("forum:post"))
        self.assertEqual(response.status_code, 200)

    def test_post_method_success_for_staff(self):
        self.client.login(email='is_staff@email.com', password='testPassword')
        response = self.client.post(reverse("forum:post"), {'title': 'test', 'text': 'txt'})
        self.assertEqual(response.status_code, 302) #302 as post redirects

    def test_post_method_success_for_non_staff(self):
        self.client.login(email='not_staff@email.com', password='testPassword')
        response = self.client.post(reverse("forum:post"), {'title': 'test', 'text': 'txt'})
        self.assertEqual(response.status_code, 302) #302 as post redirects

class TestAnnounce(TestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        get_user_model().objects.create_user(email='is_staff@email.com', password='testPassword', is_staff=True, username="test")
        get_user_model().objects.create_user(email='not_staff@email.com', password='testPassword', is_staff=False, username="test2")

    def test_access_for_staff(self):
        self.client.login(email='is_staff@email.com', password='testPassword')
        response = self.client.get(reverse("forum:announce"))
        self.assertEqual(response.status_code, 200)

    def test_access_denied_for_non_staff(self):
        self.client.login(email='not_staff@email.com', password='testPassword')
        response = self.client.get(reverse("forum:announce"))
        self.assertEqual(response.status_code, 403)

    def test_post_method_success_for_staff(self):
        self.client.login(email='is_staff@email.com', password='testPassword')
        response = self.client.post(reverse("forum:announce"), {'title': 'test', 'text': 'txt'})
        self.assertEqual(response.status_code, 302) #302 as post redirects

    def test_post_method_success_for_non_staff(self):
        self.client.login(email='not_staff@email.com', password='testPassword')
        response = self.client.post(reverse("forum:announce"), {'title': 'test', 'text': 'txt'})
        self.assertEqual(response.status_code, 403) #403 as post is denied


class TestSuggestion(TestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        get_user_model().objects.create_user(email='is_staff@email.com', password='testPassword', is_staff=True, username="test")
        get_user_model().objects.create_user(email='not_staff@email.com', password='testPassword', is_staff=False, username="test2")
        Suggestion.objects.create(poster=get_user_model().objects.get(pk=1),
                                  post_name='stest',
                                  post_text = 'stxt',
                                  post_date=timezone.now())
        Comment.objects.create(poster=get_user_model().objects.get(pk=2),
                                  comment_text = 'ctxt',
                                  post_date=timezone.now(),
                                  linked_announcement=None,
                                  linked_post=Suggestion.objects.get(id=1))
        
    def test_access_for_staff(self):
        self.client.login(email='is_staff@email.com', password='testPassword')
        response = self.client.get(reverse("forum:suggestion"), args=[1])
        self.assertEqual(response.status_code, 200)

    def test_access_denied_for_non_staff(self):
        self.client.login(email='not_staff@email.com', password='testPassword')
        response = self.client.get(reverse("forum:suggestion"), args=[1])
        self.assertEqual(response.status_code, 200)

    def test_content_displayed(self):
        self.client.login(email='is_staff@email.com', password='testPassword')
        response = self.client.get(reverse("forum:suggestion"), args=[1])
        self.assertEqual(response.context['title'], 'stest')
        self.assertEqual(len(response.context['comments']), 1)
    
class TestAnnouncement(TestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        get_user_model().objects.create_user(email='is_staff@email.com', password='testPassword', is_staff=True, username="test")
        get_user_model().objects.create_user(email='not_staff@email.com', password='testPassword', is_staff=False, username="test2")
        Annoucement.objects.create(poster=get_user_model().objects.get(pk=1),
                                  post_name='atest',
                                  post_text='atxt',
                                  post_date=timezone.now(),
                                  active=True)
        Comment.objects.create(poster=get_user_model().objects.get(pk=2),
                                  comment_text = 'ctxt',
                                  post_date=timezone.now(),
                                  linked_announcement=None,
                                  linked_post=Suggestion.objects.get(id=1))
        
    def test_access_for_staff(self):
        self.client.login(email='is_staff@email.com', password='testPassword')
        response = self.client.get(reverse("forum:announcement"), args=[1])
        self.assertEqual(response.status_code, 200)

    def test_access_denied_for_non_staff(self):
        self.client.login(email='not_staff@email.com', password='testPassword')
        response = self.client.get(reverse("forum:announcement"), args=[1])
        self.assertEqual(response.status_code, 200)

    def test_content_displayed(self):
        self.client.login(email='is_staff@email.com', password='testPassword')
        response = self.client.get(reverse("forum:announcement"), args=[1])
        self.assertEqual(response.context['title'], 'atest')
        self.assertEqual(len(response.context['comments']), 1)