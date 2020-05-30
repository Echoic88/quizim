from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.timezone import localtime, now
from .models import Quiz, PlayedQuiz, Question, PlayerAnswer, PaidQuiz


# Create your tests here.
class QuizTest(TestCase):
    def setUp(self):
        User.objects.create_user(
            username = "admin",
            password = "1290Pass"
        )

        self.user = User.objects.create_user(
            username = "test_user",
            password = "1290Pass"
        )

        self.quiz = Quiz(
            quiz_name = "test_quiz",
            creator = self.user,
        )


    def test_quiz_is_valid_with_expected_valid_data(self):
        self.quiz.save()

        self.assertEqual(self.quiz.quiz_name, "test_quiz")
        self.assertEqual(self.quiz.creator, self.user)
        self.assertIsInstance(self.quiz, Quiz)
        self.assertIsInstance(self.quiz.creator, User)
        self.assertEqual(self.quiz.instances_played, 0) # default is 0

    
    def test_raise_validation_error_if_no_quiz_name(self):
        self.quiz.quiz_name = ""
        with self.assertRaisesMessage(ValidationError, "Quiz name is required"):
            self.quiz.clean()

    
    def test_raise_validation_error_if_quiz_name_greater_than_100_characters(self):
        self.quiz.quiz_name = "x"*101
        with self.assertRaisesMessage(ValidationError, "Quiz name is too long - 100 characters maximum"):
            self.quiz.clean()


class PlayedQuizTest(TestCase):
    def setUp(self):
        User.objects.create_user(
            username = "admin",
            password = "1290Pass"
        )
        self.quiz_creator = User.objects.create(
            username="quiz_creator",
            password="12Pass90"
        )

        self.player = User.objects.create(
            username="test_user",
            password="12Pass90"
        )

        self.quiz = Quiz.objects.create(
            quiz_name="test_quiz",
            creator=self.quiz_creator
        )

        self.played_quiz_data = {
            "quiz":self.quiz,
            "player":self.player
        }


    def test_saves_with_valid_expected_data(self):
        played_quiz = PlayedQuiz(**self.played_quiz_data)
        played_quiz.save()

        self.assertIsInstance(played_quiz, PlayedQuiz)
        self.assertIsInstance(played_quiz.quiz, Quiz)
        self.assertIsInstance(played_quiz.player, User)
        

class QuestionTest(TestCase):
    def setUp(self):
        User.objects.create_user(
            username = "admin",
            password = "1290Pass"
        )
        self.user = User.objects.create(
            username = "test_user",
            password = "1290Pass",
        )
        self.quiz = Quiz.objects.create(
            quiz_name = "test_quiz",
            creator = self.user,
            created_date = localtime(now()),
        )

        self.question_data = {
            "question":"test_question",
            "correct_answer":"test_answer",
            "quiz":self.quiz
        }


    def test_question_is_saved_with_expected_valid_data(self):
        question = Question(**self.question_data)
        question.save()
        
        self.assertEqual(question.question, "test_question")
        self.assertEqual(question.correct_answer, "test_answer")
        self.assertEqual(question.quiz, self.quiz)
        self.assertEqual(question.quiz.creator, self.user)


    def test_question_is_not_saved_if_question_field_is_blank(self):
        self.question_data["question"] = ""
        question = Question(**self.question_data)
        question.save()

        try:
            q = Question.objects.get(correct_answer="test_answer")
        except:
            q = None

        self.assertNotIsInstance(q, Question)


    def test_question_is_not_saved_if_answer_field_is_blank(self):
        self.question_data["correct_answer"] = ""
        question = Question(**self.question_data)
        question.save()

        try:
            q = Question.objects.get(question="test_question")
        except:
            q = None

        self.assertNotIsInstance(q, Question)


    def test_validation_error_if_question_or_correct_answer_fields_greater_than_100_characters(self):
        self.question_data["question"] = "x"*101
        self.question_data["correct_answer"] = "x"*101

        question = Question(**self.question_data)
        with self.assertRaisesMessage(ValidationError, "Max length is 100 characters"):
            question.clean_question()
        with self.assertRaisesMessage(ValidationError, "Max length is 100 characters"):
            question.clean_correct_answer()
            

class PlayerAnswerTest(TestCase):
    
    def setUp(self):
        User.objects.create_user(
            username = "admin",
            password = "1290Pass"
        )
        self.user = User.objects.create(
            username = "test_user",
            password = "1290abyz"
        )

        self.player = User.objects.create(
            username = "test_player",
            password = "1290abyz"
        )

        self.quiz = Quiz.objects.create(
            quiz_name = "test_quiz",
            creator = self.user,
            created_date = localtime(now()),
        )

        self.question = Question.objects.create(
            question = "test_question",
            quiz = self.quiz,
            correct_answer = "test_answer"
        )

        self.answer_data = {
            "question":self.question,
            "player":self.player,
            "quiz":self.quiz,
            "player_answer":"test_player_answer",
        }

    
    def test_player_answer_is_saved_with_expected_valid_data(self):
        player_answer = PlayerAnswer(**self.answer_data)
        player_answer.save()

        self.assertEqual(player_answer.question, self.question)
        self.assertIsInstance(player_answer.question, Question)
        self.assertEqual(player_answer.player, self.player)
        self.assertIsInstance(player_answer.player, User)
        self.assertEqual(player_answer.player_answer, "test_player_answer")
        self.assertFalse(player_answer.correct) # default is False


    def test_validation_error_if_question_or_correct_answer_fields_greater_than_100_characters(self):
        self.answer_data["player_answer"] = "x"*101

        player_answer = PlayerAnswer(**self.answer_data)
        with self.assertRaisesMessage(ValidationError, "Max length is 100 characters"):
            player_answer.clean_player_answer()


    def test_if_player_answer_and_quiz_correct_answer_are_equal_then_correct_field_is_set_to_True_on_save(self):
        self.answer_data["player_answer"] = "test_answer"
        player_answer = PlayerAnswer(**self.answer_data)
        player_answer.save()
        p = PlayerAnswer.objects.get(question=self.question)

        self.assertTrue(p.correct)
        
    
    def test_that_format_answer_function_works_correctly_on_save(self):
        self.question.correct_answer = "x-men"
        self.answer_data["player_answer"] = " The X-Men"
        player_answer = PlayerAnswer(**self.answer_data)
        player_answer.save()
        p = PlayerAnswer.objects.get(question=self.question)

        self.assertTrue(p.correct)
        
    
    def test_if_player_answer_is_wrong_then_correct_field_is_False(self):
        self.answer_data["player_answer"] = "wrong_answer"
        player_answer = PlayerAnswer(**self.answer_data)
        player_answer.save()
        p = PlayerAnswer.objects.get(question=self.question)

        self.assertFalse(p.correct)
