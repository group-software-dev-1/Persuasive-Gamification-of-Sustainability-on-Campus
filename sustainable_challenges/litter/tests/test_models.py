from django.test import TestCase
from litter.models import LitterInstance
from django.contrib.auth import get_user_model
from django.utils import timezone


class TestLitterInstance(TestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        get_user_model().objects.create_user(email='test@email.com', password='testPassword')
        LitterInstance.objects.create(user=get_user_model().objects.get(pk=1),
                                        lat=53.1353531,
                                        lon=-3.2452353,
                                        img='/images/test/test_litter.jpg', 
                                        datetime=timezone.now(), 
                                        approved=0)
        
    def test_lat_label(self):
        instance = LitterInstance.objects.get(pk=1)
        field_label = instance._meta.get_field('lat').verbose_name
        self.assertEqual(field_label, 'Latitude')

    def test_lon_label(self):
        instance = LitterInstance.objects.get(pk=1)
        field_label = instance._meta.get_field('lon').verbose_name
        self.assertEqual(field_label, 'Longitude')

    def test_user_label(self):
        instance = LitterInstance.objects.get(pk=1)
        field_label = instance._meta.get_field('user').verbose_name
        self.assertEqual(field_label, 'User')
        
    def test_img_label(self):
        instance = LitterInstance.objects.get(pk=1)
        field_label = instance._meta.get_field('img').verbose_name
        self.assertEqual(field_label, 'Image')

    def test_datetime_label(self):
        instance = LitterInstance.objects.get(pk=1)
        field_label = instance._meta.get_field('datetime').verbose_name
        self.assertEqual(field_label, 'Date submitted')
    
    def test_approved_label(self):
        instance = LitterInstance.objects.get(pk=1)
        field_label = instance._meta.get_field('approved').verbose_name
        self.assertEqual(field_label, 'Approval status')

    def test_lat_max_digits(self):
        instance = LitterInstance.objects.get(pk=1)
        max_digits = instance._meta.get_field('lat').max_digits
        self.assertEqual(max_digits, 10)

    def test_lat_decimal_places(self):
        instance = LitterInstance.objects.get(pk=1)
        decimal_places = instance._meta.get_field('lat').decimal_places
        self.assertEqual(decimal_places, 7)

    def test_lon_max_digits(self):
        instance = LitterInstance.objects.get(pk=1)
        max_digits = instance._meta.get_field('lon').max_digits
        self.assertEqual(max_digits, 10)

    def test_lon_decimal_places(self):
        instance = LitterInstance.objects.get(pk=1)
        decimal_places = instance._meta.get_field('lon').decimal_places
        self.assertEqual(decimal_places, 7)
        
    def test_user_id(self):
        instance = LitterInstance.objects.get(pk=1)
        user = get_user_model().objects.get(pk=1)
        self.assertEqual(instance.user_id, user.id)

    def test_lat_default(self):
        instance = LitterInstance.objects.get(pk=1)
        default = instance._meta.get_field('lat').default
        self.assertEqual(default, 0)

    def test_lon_default(self):
        instance = LitterInstance.objects.get(pk=1)
        default = instance._meta.get_field('lon').default
        self.assertEqual(default, 0)

    def test_approved_default(self):
        instance = LitterInstance.objects.get(pk=1)
        default = instance._meta.get_field('approved').default
        self.assertEqual(default, 0)