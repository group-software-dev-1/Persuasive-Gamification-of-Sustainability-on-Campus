from django.test import TestCase
from poi.models import PlaceOfInterest, VisitedPlaceOfInterest
from django.contrib.auth import get_user_model


class TestPlaceOfInterest(TestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        PlaceOfInterest.objects.create(lat=53.1353531,
                                        lon=-3.2452353,
                                        desc="This is the description")
        
    def test_lat_label(self):
        instance = PlaceOfInterest.objects.get(pk=1)
        field_label = instance._meta.get_field('lat').verbose_name
        self.assertEqual(field_label, 'Latitude')

    def test_lon_label(self):
        instance = PlaceOfInterest.objects.get(pk=1)
        field_label = instance._meta.get_field('lon').verbose_name
        self.assertEqual(field_label, 'Longitude')

    def test_desc_label(self):
        instance = PlaceOfInterest.objects.get(pk=1)
        field_label = instance._meta.get_field('desc').verbose_name
        self.assertEqual(field_label, 'Description')
    
    def test_desc_label(self):
        instance = PlaceOfInterest.objects.get(pk=1)
        field_label = instance._meta.get_field('title').verbose_name
        self.assertEqual(field_label, 'Title')

    def test_lat_max_digits(self):
        instance = PlaceOfInterest.objects.get(pk=1)
        max_digits = instance._meta.get_field('lat').max_digits
        self.assertEqual(max_digits, 19)

    def test_lat_decimal_places(self):
        instance = PlaceOfInterest.objects.get(pk=1)
        decimal_places = instance._meta.get_field('lat').decimal_places
        self.assertEqual(decimal_places, 16)

    def test_lon_max_digits(self):
        instance = PlaceOfInterest.objects.get(pk=1)
        max_digits = instance._meta.get_field('lon').max_digits
        self.assertEqual(max_digits, 19)

    def test_lon_decimal_places(self):
        instance = PlaceOfInterest.objects.get(pk=1)
        decimal_places = instance._meta.get_field('lon').decimal_places
        self.assertEqual(decimal_places, 16)

class TestVisitedPlaceOfInterest(TestCase):
    
    @classmethod
    def setUpTestData(cls) -> None:
        get_user_model().objects.create_user(email='test@email.com', password='testPassword')
        user = get_user_model().objects.get(pk=1)
        PlaceOfInterest.objects.create(title="test title", desc="test desc", lat=50.235234, lon=-3.142535)
        poi = PlaceOfInterest.objects.get(pk=1)
        VisitedPlaceOfInterest.objects.create(user=user, place=poi)

    def test_user_label(self):
        instance = VisitedPlaceOfInterest.objects.get(pk=1)
        field_label = instance._meta.get_field('user').verbose_name
        self.assertEqual(field_label, 'User')

    def test_place_label(self):
        instance = VisitedPlaceOfInterest.objects.get(pk=1)
        field_label = instance._meta.get_field('place').verbose_name
        self.assertEqual(field_label, 'Place Of Interest')

    def test_user_id(self):
        instance = VisitedPlaceOfInterest.objects.get(pk=1)
        user = get_user_model().objects.get(pk=1)
        self.assertEqual(instance.user_id, user.id)

    
    def test_str(self):
        instance = VisitedPlaceOfInterest.objects.get(pk=1)
        expected_str = f"{instance.user} @ {instance.place}"
        self.assertEqual(str(instance), expected_str)