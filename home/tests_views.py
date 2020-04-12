from django.test import TestCase, Client
from django.shortcuts import reverse


class IndexViewTest(TestCase):
    def test_index_view_returns_correct_template(self):
        client = Client()
        response = client.get(reverse("home:index"))
        self.assertTemplateUsed(template_name="home/index.html")
        self.assertEqual(response.status_code, 200)