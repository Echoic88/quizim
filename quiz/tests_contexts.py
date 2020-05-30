from django.test import TestCase
from django.contrib.auth.models import User
from .models import Quiz, Question, PlayerAnswer
from .contexts import percentage_correct_answers, quizes_data
import uuid

class PercentageCorrectAnswerTest(TestCase):

    def setUp(self):
        User.objects.create_user(
            username = "admin",
            password = "1290Pass"
        )
        self.quiz_creator = User.objects.create(
            username="test_creator",
            password="1290Pass"
        )

        self.player = User.objects.create(
            username="test_player",
            password="1290Pass"
        )

        self.quiz = Quiz.objects.create(
            quiz_name="test_quiz",
            creator=self.quiz_creator,
        )

        Question.objects.bulk_create([
            Question(
                id = uuid.uuid4(),
                question="question1",
                correct_answer="answer1",
                quiz=self.quiz
            ),
            Question(
                id = uuid.uuid4(),
                question="question2",
                correct_answer="answer2",
                quiz=self.quiz
            ),
            Question(
                id = uuid.uuid4(),
                question="question3",
                correct_answer="answer3",
                quiz=self.quiz
            )
        ])


    def test_no_player_answers_returns_zero(self):
        self.assertEqual(percentage_correct_answers(self.player), 0)


    def test_no_questions_answered_correctly_returns_zero(self):
        # Cant use bulk create here because it will not trigger the receiver for
        # answer comparison
        PlayerAnswer.objects.create(
            id = uuid.uuid4(),
            question=Question.objects.get(question="question1"),
            player_answer="wrong",
            quiz = self.quiz,
            player = self.player,
        )
        PlayerAnswer.objects.create(
            id = uuid.uuid4(),
            question=Question.objects.get(question="question2"),
            player_answer="wrong",
            quiz = self.quiz,
            player = self.player,
        )
        PlayerAnswer.objects.create(
            id = uuid.uuid4(),
            question=Question.objects.get(question="question3"),
            player_answer="wrong",
            quiz = self.quiz,
            player = self.player,
        )

        self.assertEqual(percentage_correct_answers(self.player), 0)


    def test_all_questions_answered_correctly_returns_100(self):

        PlayerAnswer.objects.create(
            id = uuid.uuid4(),
            question=Question.objects.get(question="question1"),
            player_answer="answer1",
            quiz = self.quiz,
            player = self.player,
        )
        PlayerAnswer.objects.create(
            id = uuid.uuid4(),
            question=Question.objects.get(question="question2"),
            player_answer="answer2",
            quiz = self.quiz,
            player = self.player,
        )
        PlayerAnswer.objects.create(
            id = uuid.uuid4(),
            question=Question.objects.get(question="question3"),
            player_answer="answer3",
            quiz = self.quiz,
            player = self.player,
        )

        self.assertEqual(percentage_correct_answers(self.player), 100)


    def test_2_out_of_3_correct_return_67(self):
        # This is to test that rounding up works correctly
        PlayerAnswer.objects.create(
            id = uuid.uuid4(),
            question=Question.objects.get(question="question1"),
            player_answer="answer1",
            quiz = self.quiz,
            player = self.player,
        )
        PlayerAnswer.objects.create(
            id = uuid.uuid4(),
            question=Question.objects.get(question="question2"),
            player_answer="answer2",
            quiz = self.quiz,
            player = self.player,
        )
        PlayerAnswer.objects.create(
            id = uuid.uuid4(),
            question=Question.objects.get(question="question3"),
            player_answer="wrong",
            quiz = self.quiz,
            player = self.player,
        )

        self.assertEqual(percentage_correct_answers(self.player), 67)
