from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from poi.models import PlaceOfInterest, VisitedPlaceOfInterest
from django.urls import reverse

class TestSubmit(TestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        get_user_model().objects.create_user(email='is_staff@email.com', password='testPassword', is_staff=True, username="test")
        get_user_model().objects.create_user(email='not_staff@email.com', password='testPassword', is_staff=False, username="test2")
        PlaceOfInterest.objects.create(lat=53.1353531,
                                        lon=-3.2452353,
                                        title="test title",
                                        desc="test desc")
        PlaceOfInterest.objects.create(lat=55.1353331,
                                        lon=-3.2452311,
                                        title="test title",
                                        desc="test desc")
        
    def test_access_for_staff(self):
        self.client.login(email='is_staff@email.com', password='testPassword')
        response = self.client.get(reverse("poi:submit"))
        self.assertEqual(response.status_code, 200)

    def test_access_denied_for_non_staff(self):
        self.client.login(email='not_staff@email.com', password='testPassword')
        response = self.client.get(reverse("poi:submit"))
        self.assertEqual(response.status_code, 403)

    def test_submit_false_initally(self):
        self.client.login(email='is_staff@email.com', password='testPassword')
        response = self.client.get(reverse("poi:submit"))
        self.assertEqual(response.context['submitted'], False)

    def test_successful_post(self):
        self.client.login(email='is_staff@email.com', password='testPassword')
        response = self.client.post(reverse("poi:submit"), {'lat': 1.4256, 'lon': 34.34513, 'title': "test title", 'desc': "this is a desc"})
        self.assertEqual(response.status_code, 302)


class TestInformation(TestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        get_user_model().objects.create_user(email='is_staff@email.com', password='testPassword', is_staff=True, username="test")
        get_user_model().objects.create_user(email='not_staff@email.com', password='testPassword', is_staff=False, username="test2")
        PlaceOfInterest.objects.create(lat=53.1353531,
                                        lon=-3.2452353,
                                        title="test title",
                                        desc="test desc")
        PlaceOfInterest.objects.create(lat=55.1353331,
                                        lon=-3.2452311,
                                        title="test title",
                                        desc="test desc")
        PlaceOfInterest.objects.create(lat=58.1353331,
                                        lon=-9.2452311,
                                        title="test title",
                                        desc="test desc")
        PlaceOfInterest.objects.create(lat=40.1353331,
                                        lon=-4.2452311,
                                        title="test title",
                                        desc="test desc")

    def test_access_for_staff(self):
        self.client.login(email='is_staff@email.com', password='testPassword')
        response = self.client.get(reverse("poi:info", args=[1]))
        self.assertEqual(response.status_code, 200)

    def test_access_for_non_staff(self):
        self.client.login(email='not_staff@email.com', password='testPassword')
        response = self.client.get(reverse("poi:info", args=[1]))
        self.assertEqual(response.status_code, 200)

    def test_successful_post(self):
        self.client.login(email='not_staff@email.com', password='testPassword')
        response = self.client.post(reverse("poi:info", args=[1]), {'lat': 53.1353531, 'lon': -3.2452353})
        self.assertEqual(response.status_code, 302)
        visited = VisitedPlaceOfInterest.objects.get(user=get_user_model().objects.get(pk=2), place=PlaceOfInterest.objects.get(pk=1))
        self.assertIsNotNone(visited)

    def test_post_on_visited_is_200_response(self):
        self.client.login(email='not_staff@email.com', password='testPassword')
        response = self.client.post(reverse("poi:info", args=[2]), {'lat': 55.1353331, 'lon': -3.2452311})
        response = self.client.post(reverse("poi:info", args=[2]), {'lat': 55.1353331, 'lon': -3.2452311})
        self.assertEqual(response.context['visited'], True)
        self.assertEqual(response.status_code, 200)


class TestMap(TestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        get_user_model().objects.create_user(email='is_staff@email.com', password='testPassword', is_staff=True, username="test")
        get_user_model().objects.create_user(email='not_staff@email.com', password='testPassword', is_staff=False, username="test2")
        PlaceOfInterest.objects.create(lat=53.1353531,
                                        lon=-3.2452353,
                                        title="test title",
                                        desc="test desc")
        PlaceOfInterest.objects.create(lat=55.1353331,
                                        lon=-3.2452311,
                                        title="test title",
                                        desc="test desc")
        PlaceOfInterest.objects.create(lat=58.1353331,
                                        lon=-9.2452311,
                                        title="test title",
                                        desc="test desc")
        PlaceOfInterest.objects.create(lat=40.1353331,
                                        lon=-4.2452311,
                                        title="test title",
                                        desc="test desc")
        
    def test_access_for_staff(self):
        self.client.login(email='is_staff@email.com', password='testPassword')
        response = self.client.get(reverse("poi:map"))
        self.assertEqual(response.status_code, 200)

    def test_access_for_non_staff(self):
        self.client.login(email='not_staff@email.com', password='testPassword')
        response = self.client.get(reverse("poi:map"))
        self.assertEqual(response.status_code, 200)

    def test_4_poi_in_json_dict(self):
        self.client.login(email='not_staff@email.com', password='testPassword')
        response = self.client.get(reverse("poi:map"))
        self.assertEqual(len(response.context['json_dict']['places']), 4)

