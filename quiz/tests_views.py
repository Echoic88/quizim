from django.test import TestCase, Client, RequestFactory
from django.shortcuts import reverse
from django.contrib.auth.models import User
from .models import Quiz, Question
from .forms import QuizForm, CreateQuestionModelFormSet, EditQuestionModelFormSet
from .views import create_quiz
import uuid

class CreateQuizViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        cls.user = User.objects.create(
            username="test_user",
            password="12Pass90"
        )

    def test_get_response_returns_correct_template(self):
        response = self.client.get(reverse("quiz:create_quiz"))
        
        self.assertTemplateUsed(response, template_name="quiz/create-quiz.html")
        self.assertEqual(response.status_code, 200)


    def test_get_response_returns_quiz_form_and_create_questions_formset(self):
        response = self.client.get(reverse("quiz:create_quiz"))

        quiz_form = response.context["quiz_form"]
        questions_formset = response.context["questions_formset"]
        self.assertIsInstance(quiz_form, QuizForm)
        self.assertIsInstance(questions_formset, CreateQuestionModelFormSet)


class EditQuizViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        cls.user = User.objects.create(
            username="test_user",
            password="12Pass90"
        )
        cls.quiz = Quiz.objects.create(
            quiz_name="test_quiz",
            creator=cls.user
        )
        cls.questions = Question.objects.bulk_create([
            Question(
                id = uuid.uuid4(),
                question="question1",
                correct_answer="answer1",
                quiz=cls.quiz
            ),
            Question(
                id = uuid.uuid4(),
                question="question2",
                correct_answer="answer2",
                quiz=cls.quiz
            ),
            Question(
                id = uuid.uuid4(),
                question="question3",
                correct_answer="answer3",
                quiz=cls.quiz
            )
        ])


    def test_get_response_returns_correct_template(self):
        print(self.questions)
        response = self.client.get(reverse("quiz:edit_quiz", args=[self.quiz.id]))
        
        self.assertTemplateUsed(response, template_name="quiz/edit-quiz.html")
        self.assertEqual(response.status_code, 200)


    def test_get_response_returns_correct_template(self):
        response = self.client.get(reverse("quiz:edit_quiz", args=[self.quiz.id]))
        
        self.assertTemplateUsed(response, template_name="quiz/edit-quiz.html")
        self.assertEqual(response.status_code, 200)


    def test_get_response_returns_edit_questions_formset(self):
        response = self.client.get(reverse("quiz:edit_quiz", args=[self.quiz.id]))

        formset = response.context["formset"]
        self.assertIsInstance(formset, EditQuestionModelFormSet)
