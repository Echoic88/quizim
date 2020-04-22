from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from .forms import UserUpdateForm

class UserUpdateFormTest(TestCase):

    def test_user_saves_with_expected_valid_data(self):
        data = {
            "username":"test_user",
            "email":"test_mail@test.tes"
        }
        form = UserUpdateForm(data=data)
        f = form.save()

        self.assertTrue(form.is_valid())
        self.assertIsInstance(f, User)


    def test_raise_ValidationError_if_username_is_missing(self):
        data = {
            "username":"",
            "email":"test_mail@test.tes"
        }

        form = UserUpdateForm(data=data)
        self.assertFalse(form.is_valid())


    def test_raise_error_if_email_is_missing(self):
        data = {
            "username":"test_user",
            "email":""
        }

        form = UserUpdateForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["email"], ["This field is required.",])
