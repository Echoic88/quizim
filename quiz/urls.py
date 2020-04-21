from django.urls import path
from .views import index, create_quiz, edit_quiz

app_name = "quiz"
urlpatterns = [
    path("", index, name="index"),
    path("create-quiz/", create_quiz, name="create_quiz"),
    path("edit-quiz/<uuid:id>", edit_quiz, name="edit_quiz"),
]