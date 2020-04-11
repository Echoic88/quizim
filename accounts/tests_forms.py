from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Profile
from .forms import ProfileForm

class ProfileFormTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        """
        Set up the base data for tests
        Save a new User creating a corresponding Profile 
        which is then retrieved
        """
        cls.user = User(
            username="test",
            password="12Pass90"
        )
        cls.user.save()
        cls.profile = Profile.objects.get(user=cls.user)


    def setUp(self):
        # base form data (which is valid) for tests
        self.form_data = {
            "address1":"test",
            "address2":"test",
            "city":"test",
            "postcode":"1234abc",
            #below is a valid country code for use with django-countries
            "country":"IE", 
            "profile_pic":"./test_pictures/test_pic.jpg",
            "receive_email":True,
        }


    def test_form_is_valid_with_expected_valid_data(self):
        data = self.form_data
        form = ProfileForm(instance=self.profile, data=data)
        self.assertTrue(form.is_valid())
        self.assertEqual(self.profile.user, self.user)


    def test_form_is_valid_with_no_data(self):
        data = {}
        form = ProfileForm(instance=self.profile, data=data)
        self.assertTrue(form.is_valid())


    def test_form_raises_validation_error_if_address1_greater_than_100_characters(self):
        data = self.form_data
        data["address1"] = "x"*101
        form = ProfileForm(instance=self.profile, data=data)
        self.assertFalse(form.is_valid())
        self.assertRaises(ValidationError)


    def test_form_raises_validation_error_if_address2_greater_than_100_characters(self):
        data = self.form_data
        data["address2"] = "x"*101
        form = ProfileForm(instance=self.profile, data=data)
        self.assertFalse(form.is_valid())
        self.assertRaises(ValidationError)


    def test_form_raises_validation_error_if_city_greater_than_100_characters(self):
        self.form_data["city"] = "x"*101
        form = ProfileForm(instance=self.profile, data=self.form_data)
        self.assertFalse(form.is_valid())
        self.assertRaises(ValidationError)


    def test_form_raises_validation_error_if_postcode_greater_than_10_characters(self):
        self.form_data["postcode"] = "x"*11
        form = ProfileForm(instance=self.profile, data=self.form_data)
        self.assertFalse(form.is_valid())
        self.assertRaises(ValidationError)


# Delete the below later
"""
    def test_form_is_valid_with_expected_valid_data2(self):
        # When a new User is saved a corresponding Profile
        # is created
        user =  User(
            username="test1",
            password="12Pass90"
        )
        user.save()
        profile = Profile.objects.get(user=user)

        form_data = {
            "address1":"x"*101,
            "address2":"test",
            "city":"test",
            "postcode":"1234abc",
            #below is a valid country code for use with django-countries
            "country":"IE", 
            "profile_pic":"./test_pictures/test_pic.jpg",
            "receive_email":True,
        }

        form = ProfileForm(instance=profile, data=form_data)
        self.assertFalse(form.is_valid())
        self.assertRaises(ValidationError)
"""