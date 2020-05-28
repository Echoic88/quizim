from django.test import TestCase, Client, RequestFactory
from django.contrib.auth.models import User, AnonymousUser
from django.shortcuts import reverse
from .views import index


class UserAreaIndexViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username="test_user",
            email="test_email@test.com",
            password="1290Pass"
        )

    def test_get_response_code_with_logged_in_user(self):
        request = self.factory.get("userarea:index")
        request.user = self.user
        response = index(request)
        self.assertEqual(response.status_code, 200)
