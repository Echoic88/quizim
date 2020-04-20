from django.shortcuts import render, redirect, reverse
from .forms import QuizForm, CreateQuestionModelFormSet, EditQuestionModelFormSet, PlayerAnswerModelFormSet
from .models import Question, Quiz, PlayerAnswer
from django.contrib.auth.models import User


# Create your views here.

def index(request):
    """
    Temporary home page for testing quiz links
    """
    quizes = Quiz.objects.all() or None
    return render(request, "quiz/index.html", {
        "quizes":quizes
    })


def create_quiz(request):
    """
    Create a new quiz
    """
    if request.method == "POST":
        quiz_form = QuizForm(request.POST)
        questions_formset = CreateQuestionModelFormSet(request.POST)

        if quiz_form.is_valid():
             q = quiz_form.save(commit=False)
             q.creator = request.user
             q.save()

        
        if questions_formset.is_valid():
            for form in questions_formset:
                f = form.save(commit=False)
                f.quiz = q
                f.save()

        return redirect(reverse("quiz:index"))


    else:
        quiz_form = QuizForm()
        questions_formset = CreateQuestionModelFormSet()
    
    return render(request, "quiz/create-quiz.html", {
        "quiz_form":quiz_form,
        "questions_formset":questions_formset
    })
    
