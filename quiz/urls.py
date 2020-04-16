from django.urls import path
from .views import index, create_quiz, edit_quiz, play_quiz, quiz_result, delete_player_answers

app_name = "formsets_medium"
urlpatterns = [
    path("", index, name="index"),
    path("create_quiz/", create_quiz, name="create_quiz"),
    path("play_quiz/<int:id>", play_quiz, name="play_quiz"),
    path("edit_quiz/<int:id>", edit_quiz, name="edit_quiz"),
    path("quiz_result/<int:id>", quiz_result, name="quiz_result"),
    path("delete_temp", delete_player_answers, name="delete_temp"),

]