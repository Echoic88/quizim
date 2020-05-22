from django.shortcuts import render, redirect, reverse
from quiz.models import Quiz

# Create your views here.
def index(request):
    """
    Display home/index.html for the home page
    """
    # Question men list is a list of the images used for individual quizes 
    question_man_list = []
    for i in range(4):
        question_man_list.append("images/question-man{0}.png".format(i))

    quizes = Quiz.objects.all()
    return render(request, "home/index.html", {
        "question_man_list":question_man_list,
        "quizes":quizes
    })
