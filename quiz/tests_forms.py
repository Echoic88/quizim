from django.test import TestCase
from django.utils.timezone import localtime, now
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Quiz, Question, PlayerAnswer
from .forms import QuizForm, QuestionForm, CreateQuestionModelFormSet, EditQuestionModelFormSet, PlayerAnswerModelFormSet
import uuid


class QuizFormTest(TestCase):
    
    def setUp(self):
        self.user = User.objects.create(
            username="test_user",
            password="12Pass90"
        )

    
    def test_quiz_saves_with_expected_valid_data(self):
        form = QuizForm({
            "quiz_name":"test_quiz"
        })
        f = form.save(commit=False)
        f.creator = self.user
        f.save()

        self.assertTrue(form.is_valid())
        self.assertIsInstance(f, Quiz)
        self.assertIsInstance(f.creator, User)
        self.assertEqual(f.quiz_name, "test_quiz")
        self.assertEqual(f.creator, self.user)
        self.assertEqual(f.instances_played, 0)


    def test_raise_ValidationError_if_quiz_name_is_blank(self):
        form = QuizForm({
            "quiz_name":""
        })

        self.assertFalse(form.is_valid())
        self.assertRaises(ValidationError)


    def test_raise_ValidationError_if_quiz_name_is_greater_than_100_characters(self):
        form = QuizForm({
            "quiz_name":"x"*101
        })

        self.assertFalse(form.is_valid())
        self.assertRaises(ValidationError)


class QuestionFormTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(
            username="test_user",
            password="12Pass90"
        )

        self.quiz = Quiz.objects.create(
            quiz_name="test_quiz",
            creator = self.user
        )

        self.question_data = {
            "question":"test_question",
            "correct_answer":"test_answer"
        }


    def test_question_saves_with_expected_valid_data(self):
        form = QuestionForm(data=self.question_data)    
        
        f = form.save(commit=False)
        f.quiz = self.quiz
        f.save()

        self.assertTrue(form.is_valid())
        self.assertIsInstance(f, Question)
        self.assertEqual(f.question, "test_question")
        self.assertEqual(f.correct_answer, "test_answer")
        self.assertIsInstance(f.quiz, Quiz)
        self.assertEqual(f.quiz, self.quiz)


    def test_form_is_valid_with_blank_question_but_does_not_save_question_instance(self):
        """
        Question instances with blank question should still be valid
        but the pre_save receiver will prevent save
        Only forms submitted with both a question and answer should 
        save successfully to the database. Explanation in Question model
        """
        self.question_data["question"] = ""
        form = QuestionForm(data=self.question_data)
        f = form.save(commit=False)
        f.quiz = self.quiz
        question_id = f.id
        f.save()

        question_exists = Question.objects.filter(id=question_id).exists()

        self.assertTrue(form.is_valid())
        self.assertFalse(question_exists)


    def test_form_is_valid_with_blank_answer_but_does_not_save_question_instance(self):
        """
        Question instances with blank answer should still be valid
        but the pre_save receiver will prevent save
        Only forms submitted with both a question and answer should 
        save successfully to the database. Explanation in Question model
        """
        self.question_data["correct_answer"] = ""
        form = QuestionForm(data=self.question_data)
        f = form.save(commit=False)
        f.quiz = self.quiz
        question_id = f.id
        f.save()

        question_exists = Question.objects.filter(id=question_id).exists()

        self.assertTrue(form.is_valid())
        self.assertFalse(question_exists)

    
    def test_form_is_valid_with_both_blank_question_and_answer_but_does_not_save_question_instance(self):
        """
        Question instances with blank question and answer 
        should still be valid but the pre_save receiver will prevent save
        Only forms submitted with both a question and answer should 
        save successfully to the database. Explanation in Question model
        """
        self.question_data["question"] = ""
        self.question_data["correct_answer"] = ""

        form = QuestionForm(data=self.question_data)
        f = form.save(commit=False)
        question_id = f.id
        f.save()

        question_exists = Question.objects.filter(id=question_id).exists()

        self.assertTrue(form.is_valid())
        self.assertFalse(question_exists)


class CreateQuestionModelFormSetTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(
            username="test_user",
            password="12Pass90"
        )

        self.quiz = Quiz.objects.create(
            quiz_name="test_quiz",
            creator = self.user
        )

        self.formset_data = {
            "form-TOTAL_FORMS": "3",
            "form-INITIAL_FORMS": "0",
            "form-MAX_NUM_FORMS": "",
            "form-0-question": "x"*100,
            "form-0-correct_answer":"x"*100,
            "form-1-question": "y"*100,
            "form-1-correct_answer":"y"*100,
            "form-2-question": "z"*100,
            "form-2-correct_answer":"z"*100,
        }


    def test_formset_is_valid_with_expected_valid_data(self):
        formset = CreateQuestionModelFormSet(data=self.formset_data)

        self.assertTrue(formset.is_valid())
        

class EditQuestionModelFormSetTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(
            username="test_user",
            password="12Pass90"
        )

        self.quiz = Quiz.objects.create(
            quiz_name="test_quiz",
            creator = self.user
        )

        self.formset_data = {
            "form-TOTAL_FORMS": "3",
            "form-INITIAL_FORMS": "0",
            "form-MAX_NUM_FORMS": "",
            "form-0-question": "x"*100,
            "form-0-correct_answer":"x"*100,
            "form-1-question": "y"*100,
            "form-1-correct_answer":"y"*100,
            "form-2-question": "z"*100,
            "form-2-correct_answer":"z"*100,
        }


    def test_formset_is_valid_with_expected_valid_data(self):
        formset = EditQuestionModelFormSet(data=self.formset_data)
        
        self.assertTrue(formset.is_valid())
