from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Profile


# Create your tests here.


class ProfileTest(TestCase):
    """
    Test the Profile model
    """
    def setUp(self):
        """
        Set up a base User instance for tests
        """
        self.user = User(
            username = "test_user",
            password = "1290abyz"
        )
        self.user.save()
        self.profile = Profile.objects.get(user=self.user)

        test_pic = "./test_pictures/test_pic.jpg"
        self.profile_data = {
            "address1":"address1",
            "address2":"address2",
            "city":"city",
            "postcode":"12345",
            "country":"Ireland",
            "profile_pic":test_pic,
        }

    
    def test_profile_instance_is_created_when_user_is_created(self):
        self.assertIsInstance(self.profile, Profile)
        #test that the Profile instance matches the User instance
        self.assertIsInstance(self.profile.user, User)


    def test_instance_is_valid_with_expected_valid_data(self):
        data = self.profile_data      
        Profile.objects.update(user=self.user, **data)
        profile = Profile.objects.get(user=self.user)

        self.assertIsInstance(profile, Profile)
        self.assertIsInstance(profile.user, User)
        self.assertEqual(profile.address1, "address1")
        self.assertEqual(profile.address2, "address2")
        self.assertEqual(profile.city, "city")
        self.assertEqual(profile.postcode, "12345")
        self.assertEqual(profile.country, "Ireland")
        self.assertEqual(profile.profile_pic, "./test_pictures/test_pic.jpg")
        self.assertEqual(profile.receive_email, False)


    def test_instance_is_valid_if_non_required_fields_are_omitted(self):
        data = {
            "address1":"",
            "address2":"",
            "city":"",
            "postcode":"",
            "country":"",
            "profile_pic":"",
        }     
        Profile.objects.update(user=self.user, **data)
        profile = Profile.objects.get(user=self.user)
        
        self.assertEqual(profile.address1, "")
        self.assertEqual(profile.address2, "")
        self.assertEqual(profile.city, "")
        self.assertEqual(profile.postcode, "")
        self.assertEqual(profile.country, "")
        self.assertEqual(profile.profile_pic, "")
        self.assertEqual(profile.receive_email, False) #default to False
        self.assertIsInstance(profile, Profile)


    def test_raise_ValidationError_when_address1_greater_than_100_characters(self):
        data = self.profile_data
        data["address1"] = "x"*101
        Profile.objects.update(user=self.user, **data)
        profile = Profile.objects.get(user=self.user)
        with self.assertRaisesMessage(ValidationError, "Max length is 100 characters"):
            profile.clean()
    

    def test_raise_ValidationError_when_address2_greater_than_100_characters(self):
        data = self.profile_data
        data["address2"] = "x"*101
        Profile.objects.update(user=self.user, **data)
        profile = Profile.objects.get(user=self.user)
        with self.assertRaisesMessage(ValidationError, "Max length is 100 characters"):
            profile.clean()


    def test_raise_ValidationError_when_city_greater_than_100_characters(self):
        data = self.profile_data
        data["city"] = "x"*101
        Profile.objects.update(user=self.user, **data)
        profile = Profile.objects.get(user=self.user)
        with self.assertRaisesMessage(ValidationError, "Max length is 100 characters"):
            profile.clean()

        
    def test_raise_ValidationError_when_postcode_greater_than_10_characters(self):
        data = self.profile_data
        data["postcode"] = "x"*11
        Profile.objects.update(user=self.user, **data)
        profile = Profile.objects.get(user=self.user)
        with self.assertRaisesMessage(ValidationError, "Max length is 10 characters"):
            profile.clean()

    
    def test_raise_ValidationError_when_country_is_not_in_django_countries_list(self):
        data = self.profile_data
        data["country"] = "Invalid"
        Profile.objects.update(user=self.user, **data)
        profile = Profile.objects.get(user=self.user)
        with self.assertRaisesMessage(ValidationError, "This is not a valid country"):
            profile.clean()
        

    def test_raise_ValidationError_if_profile_pic_is_not_JPEG_or_PNG_type(self):
        data = self.profile_data
        print(data["profile_pic"])
        #data["profile_pic"] = "./test_pictures/test_text_file.txt"
        Profile.objects.update(user=self.user, **data)
        profile = Profile.objects.get(user=self.user)
        with self.assertRaises(ValidationError):
            profile.clean()

    