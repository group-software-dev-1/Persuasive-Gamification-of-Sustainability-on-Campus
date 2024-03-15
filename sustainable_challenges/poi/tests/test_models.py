from django.test import TestCase
from poi.models import PlaceOfInterest


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

    def test_lat_max_digits(self):
        instance = PlaceOfInterest.objects.get(pk=1)
        max_digits = instance._meta.get_field('lat').max_digits
        self.assertEqual(max_digits, 10)

    def test_lat_decimal_places(self):
        instance = PlaceOfInterest.objects.get(pk=1)
        decimal_places = instance._meta.get_field('lat').decimal_places
        self.assertEqual(decimal_places, 7)

    def test_lon_max_digits(self):
        instance = PlaceOfInterest.objects.get(pk=1)
        max_digits = instance._meta.get_field('lon').max_digits
        self.assertEqual(max_digits, 10)

    def test_lon_decimal_places(self):
        instance = PlaceOfInterest.objects.get(pk=1)
        decimal_places = instance._meta.get_field('lon').decimal_places
        self.assertEqual(decimal_places, 7)

    def test_lat_default(self):
        instance = PlaceOfInterest.objects.get(pk=1)
        default = instance._meta.get_field('lat').default
        self.assertEqual(default, 0)

    def test_lon_default(self):
        instance = PlaceOfInterest.objects.get(pk=1)
        default = instance._meta.get_field('lon').default
        self.assertEqual(default, 0)
    
    def test_desc_default(self):
        instance = PlaceOfInterest.objects.get(pk=1)
        default = instance._meta.get_field('desc').default
        self.assertEqual(default, "")