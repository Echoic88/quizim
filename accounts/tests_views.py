from django.test import TestCase, Client
from django.shortcuts import reverse
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from .forms import SignUpForm 


class SignUpViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()


    def setUp(self):
        self.signup_data = {
            "username":"testuser",
            "password1":"12Pass90",
            "password2":"12Pass90"
        }


    def test_signup_view_returns_correct_template(self):
        response = self.client.get(reverse("accounts:signup"))
        self.assertTemplateUsed(response, template_name="accounts/signup.html")
        self.assertEqual(response.status_code, 200)


    def test_data_posted_through_form_redirects_to_registration_success_on_complete(self):
        response = self.client.post(reverse("accounts:signup"), data=self.signup_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("accounts:signup_success"))


    def test_valid_data_posted_creates_a_User(self):
        response = self.client.post(reverse("accounts:signup"), data=self.signup_data)
        self.assertTrue(User.objects.get(username = self.signup_data["username"]))


    def test_if_user_with_this_username_already_exists_and_raise_message(self):
        # before the post response create a User instance with the same username to compare against
        User.objects.create(
            username = self.signup_data["username"],
            password = "1290Pass"
        )

        response = self.client.post(reverse("accounts:signup"), data=self.signup_data)
        # below from stack overflow
        # https://stackoverflow.com/questions/2897609/how-can-i-unit-test-django-messages
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'This username is taken. Please choose another one')


    def test_where_user_has_chosen_existing_username_that_the_existing_User_object_isnt_modified(self):
        User.objects.create(
            username = self.signup_data["username"],
            password = "1290Pass"
        )
        user_before = User.objects.get(username=self.signup_data["username"])
        response = self.client.post(reverse("accounts:signup"), data=self.signup_data)
        user_after = User.objects.get(username=self.signup_data["username"])
        self.assertEqual(user_before, user_after)


    def test_on_user_registration_set_is_active_to_false(self):
        response = self.client.post(reverse("accounts:signup"), data=self.signup_data)
        user = User.objects.get(username=self.signup_data["username"])
        # the newly created user object should be set to false
        # user will confirm registration by email 
        self.assertFalse(user.is_active)


class SignUpSuccessViewTest(TestCase):
    def test_view_display_correct_page(self):
        client = Client()
        response = client.get(reverse("accounts:signup_success"))
        self.assertTemplateUsed(response, template_name="accounts/signup-success.html")
        self.assertEqual(response.status_code, 200)
