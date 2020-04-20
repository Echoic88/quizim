from django.test import TestCase, Client, RequestFactory
from django.shortcuts import reverse
from django.contrib.auth.models import User
from .models import Quiz
from .forms import QuizForm, CreateQuestionModelFormSet
from .views import create_quiz

class CreateQuizViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        cls.user = User.objects.create(
            username="test_user",
            password="12Pass90"
        )


    def setUp(self):
        self.factory = RequestFactory()


    def test_get_response_returns_correct_template(self):
        response = self.client.get(reverse("quiz:create_quiz"))
        
        self.assertTemplateUsed(response, template_name="quiz/create-quiz.html")
        self.assertEqual(response.status_code, 200)


    def test_get_response_returns_quiz_form_and_questions_formset(self):
        response = self.client.get(reverse("quiz:create_quiz"))

        quiz_form = response.context["quiz_form"]
        questions_formset = response.context["questions_formset"]
        self.assertIsInstance(quiz_form, QuizForm)
        self.assertIsInstance(questions_formset, CreateQuestionModelFormSet)
