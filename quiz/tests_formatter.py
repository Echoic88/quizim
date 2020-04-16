from django.test import TestCase
from .formatter import format_answer

class FormatAnswerTest(TestCase):

    def test_formatter_removes_article_word_a(self):
        test_string = "a test"
        self.assertEqual(format_answer(test_string), "test")

    
    def test_formatter_removes_article_word_A(self):
        test_string = "A test"
        self.assertEqual(format_answer(test_string), "test")

    
    def test_formatter_removes_article_word_the(self):
        test_string = "the test"
        self.assertEqual(format_answer(test_string), "test")


    def test_formatter_removes_article_word_The(self):
        test_string = "The test"
        self.assertEqual(format_answer(test_string), "test")


    def test_formatter_removes_article_word_an(self):
        test_string = "An test"
        self.assertEqual(format_answer(test_string), "test")


    def test_formatter_removes_article_word_An(self):
        test_string = "An test"
        self.assertEqual(format_answer(test_string), "test")


    def test_formatter_removes_spaces_at_begining_and_end_of_string(self):
        test_string = " An test "
        self.assertEqual(format_answer(test_string), "test")

    def test_formatter_removes_spaces_between_words(self):
        test_string = "This is a Test For Spaces"
        self.assertEqual(format_answer(test_string), "thisisatestforspaces")


    def test_formatter_converts_to_lower_case(self):
        test_string = " AN TEST "
        self.assertEqual(format_answer(test_string), "test")


    def test_removes_non_alphanumeric(self):
        test_string = "AN TEST?!.£$%^&*()-=_+[];':@#~,.<>/?\|"
        self.assertEqual(format_answer(test_string), "test")


    def test_doesnt_remove_numbers(self):
        test_string = "1234567890"
        self.assertEqual(format_answer(test_string), "1234567890")
