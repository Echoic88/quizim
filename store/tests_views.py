from django.test import TestCase, Client
from django.shortcuts import reverse
from .views import index

# Create your tests here.
class IndexViewTest(TestCase):

    def test_view_displays_correct_page(self):
        client = Client()
        response = client.get(reverse("store:index"))
        self.assertTemplateUsed(response, template_name="store/index.html")
        self.assertEqual(response.status_code, 200)

