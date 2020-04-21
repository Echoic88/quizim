from django.urls import path
from .views import index, create_quiz, edit_quiz, play_quiz, quiz_result

app_name = "quiz"
urlpatterns = [
    path("", index, name="index"),
    path("create-quiz/", create_quiz, name="create_quiz"),
    path("edit-quiz/<uuid:id>", edit_quiz, name="edit_quiz"),
    path("play_quiz/<uuid:id>", play_quiz, name="play_quiz"),
    path("quiz_result/<uuid:id>", quiz_result, name="quiz_result"),
]

