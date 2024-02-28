from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from litter.models import LitterInstance
from django.urls import reverse

class TestLatest(TestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        get_user_model().objects.create_user(email='is_staff@email.com', password='testPassword', is_staff=True)
        get_user_model().objects.create_user(email='not_staff@email.com', password='testPassword', is_staff=False)
        LitterInstance.objects.create(user=get_user_model().objects.get(pk=1),
                                        lat=53.1353531,
                                        lon=-3.2452353,
                                        img='/images/test/test_litter.jpg', 
                                        datetime=timezone.now(), 
                                        approved=0)
        LitterInstance.objects.create(user=get_user_model().objects.get(pk=1),
                                        lat=55.1353331,
                                        lon=-3.2452311,
                                        img='/images/test/test_litter.jpg', 
                                        datetime=timezone.now(), 
                                        approved=0)
        LitterInstance.objects.create(user=get_user_model().objects.get(pk=2),
                                        lat=53.1353121,
                                        lon=-3.2454353,
                                        img='/images/test/test_litter.jpg', 
                                        datetime=timezone.now(), 
                                        approved=0)
        LitterInstance.objects.create(user=get_user_model().objects.get(pk=2),
                                        lat=53.1353935,
                                        lon=-3.2452013,
                                        img='/images/test/test_litter.jpg', 
                                        datetime=timezone.now(), 
                                        approved=1)
        
    def test_access_for_staff(self):
        self.client.login(email='is_staff@email.com', password='testPassword')
        response = self.client.get(reverse("litter:latest"))
        self.assertEqual(response.status_code, 200)

    def test_access_denied_for_non_staff(self):
        self.client.login(email='not_staff@email.com', password='testPassword')
        response = self.client.get(reverse("litter:latest"))
        self.assertEqual(response.status_code, 403)

    def test_staff_gets_4_instances(self):
        self.client.login(email='is_staff@email.com', password='testPassword')
        response = self.client.get(reverse("litter:latest"))
        self.assertEqual(len(response.context['latest_instance_list']), 3)


class TestInstance(TestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        get_user_model().objects.create_user(email='is_staff@email.com', password='testPassword', is_staff=True)
        get_user_model().objects.create_user(email='not_staff@email.com', password='testPassword', is_staff=False)
        LitterInstance.objects.create(user=get_user_model().objects.get(pk=1), # Instance made by staff user
                                        lat=53.1353531,
                                        lon=-3.2452353,
                                        img='/images/test/test_litter.jpg', 
                                        datetime=timezone.now(), 
                                        approved=0)
        LitterInstance.objects.create(user=get_user_model().objects.get(pk=2), # Instance made by non-staff user
                                        lat=53.1353121,
                                        lon=-3.2454353,
                                        img='/images/test/test_litter.jpg', 
                                        datetime=timezone.now(), 
                                        approved=0)
        
    def test_access_for_staff_on_not_their_own_report(self):
        self.client.login(email='is_staff@email.com', password='testPassword')
        response = self.client.get(reverse("litter:instance", args=[2]))
        self.assertEqual(response.status_code, 200)

    def test_access_for_staff_on_their_own_report(self):
        self.client.login(email='is_staff@email.com', password='testPassword')
        response = self.client.get(reverse("litter:instance", args=[1]))
        self.assertEqual(response.status_code, 200)

    def test_access_denied_for_non_staff_on_not_their_own_report(self):
        self.client.login(email='not_staff@email.com', password='testPassword')
        response = self.client.get(reverse("litter:instance", args=[1]))
        self.assertEqual(response.status_code, 403)

    def test_access_for_non_staff_on_their_own_report(self):
        self.client.login(email='not_staff@email.com', password='testPassword')
        response = self.client.get(reverse("litter:instance", args=[2]))
        self.assertEqual(response.status_code, 200)

    def test_non_staff_cannot_approve_their_own_report(self):
        self.client.login(email='not_staff@email.com', password='testPassword')
        response = self.client.post(reverse("litter:instance", args=[2]), {'options': 1})
        self.assertEqual(response.status_code, 403)

    def test_staff_cannot_approve_their_own_report(self):
        self.client.login(email='is_staff@email.com', password='testPassword')
        response = self.client.post(reverse("litter:instance", args=[1]), {'options': 1})
        self.assertEqual(response.status_code, 403)

    def test_staff_can_approve_someone_elses_report(self):
        self.client.login(email='is_staff@email.com', password='testPassword')
        response = self.client.post(reverse("litter:instance", args=[2]), {'options': 1})
        self.assertEqual(response.status_code, 302) # 302 because of the redirection

    def test_staff_approving_a_report_gives_it_the_correct_approval_status(self):
        self.client.login(email='is_staff@email.com', password='testPassword')
        response = self.client.post(reverse("litter:instance", args=[2]), {'options': 2})
        self.assertEqual(LitterInstance.objects.get(pk=2).approved, 2)
        response = self.client.post(reverse("litter:instance", args=[2]), {'options': 1})
        self.assertEqual(LitterInstance.objects.get(pk=2).approved, 1)


class TestReport(TestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        get_user_model().objects.create_user(email='is_staff@email.com', password='testPassword', is_staff=True)
        get_user_model().objects.create_user(email='not_staff@email.com', password='testPassword', is_staff=False)

    def test_access_for_staff(self):
        pass

    def test_access_for_non_staff(self):
        pass

    def test_post_method_for_staff(self):
        pass

    def test_post_method_for_non_staff(self):
        pass

    