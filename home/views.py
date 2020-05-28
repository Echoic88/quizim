from django.shortcuts import render, redirect, reverse
from quiz.models import Quiz, PlayedQuiz, User

# Create your views here.
def index(request):
    """
    Display home/index.html for the home page
    """
    # Question men list is a list of the images used for individual quizes 
    question_man_list = []
    for i in range(4):
        question_man_list.append("images/question-man{0}.png".format(i))

    # quizes created by admin should be excluded since admin creates quizes to be used in-store
    quizes = Quiz.objects.exclude(creator=request.user).exclude(creator=User.objects.get(username="admin"))

    if request.user.is_authenticated:
        played_quizes = PlayedQuiz.objects.filter(player=request.user)
        played_quizes_list = []
        for quiz in quizes:
            for played in played_quizes:
                if quiz == played.quiz:
                    played_quizes_list.append(quiz)

    return render(request, "home/index.html", {
        "question_man_list":question_man_list,
        "quizes":quizes,
        "played_quizes_list":played_quizes_list
    })
