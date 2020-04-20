from django.urls import path
from .views import index, create_quiz

app_name = "quiz"
urlpatterns = [
    path("", index, name="index"),
    path("create_quiz/", create_quiz, name="create_quiz"),   
]