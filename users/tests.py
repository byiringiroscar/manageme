from django.test import TestCase
from users.models import Property_registration, User


# Create your tests here.


class RegistrationTest(TestCase):

    def setUp(self):
        user = User.objects.all().first()

        Property_registration.objects.create(property_name="Car", location="kigali",
                                             property_type="car", amount_per_month=50000,
                                             detail="good property and heavy turbo", property_image='image/oscar.jpg',
                                             available=True, owner_name=user)

        def test_get_property_name(self):
            name = Property_registration.objects.get(id=1)
            field_label = name._meta.get_field('property_name').verbose_name
            self.assertEqual(field_label, 'property_name')

        def test_availability(self):
            prop_available = Property_registration.objects.get(id=1)
            field_label = prop_available._meta.get_field('available').verbose_name
            self.assertEqual(field_label, 'available')
