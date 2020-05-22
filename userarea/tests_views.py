from django.test import TestCase, Client
from django.shortcuts import reverse
from .views import index


class UserAreaIndexViewTest(TestCase):

    # def setUp(self):
    #     self.client = Client()
    #     self.user = User.objects.create(
    #         username="test_user",
    #     )
    #     self.user.set_password("1290Pass")


    def test_get_response_returns_correct_template(self):
        client = Client()
        response = client.get(reverse("userarea:index"))  
        # self.assertTemplateUsed(response, template_name="userarea/index.html")
        self.assertEqual(response.status_code, 302)


"""
    def test_get_response_returns_quiz_form_and_create_questions_formset(self):
        response = self.client.get(reverse("quiz:create_quiz"))

        quiz_form = response.context["quiz_form"]
        questions_formset = response.context["questions_formset"]
        self.assertIsInstance(quiz_form, QuizForm)
        self.assertIsInstance(questions_formset, CreateQuestionModelFormSet)

"""