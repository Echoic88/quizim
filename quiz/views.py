from django.shortcuts import render, redirect, reverse
from .forms import QuizForm, CreateQuestionModelFormSet, EditQuestionModelFormSet, PlayerAnswerModelFormSet
from .models import Question, Quiz, PlayerAnswer
from django.contrib.auth.models import User
import uuid


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
                f.id = uuid.uuid4()
                f.quiz = q
                f.save()

        return redirect(reverse("quiz:index"))


    else:
        quiz_form = QuizForm()
        questions_formset = CreateQuestionModelFormSet(queryset = Question.objects.none())
        
    return render(request, "quiz/create-quiz.html", {
        "quiz_form":quiz_form,
        "questions_formset":questions_formset
    })
    

def edit_quiz(request, id):
    """
    Edit an existing quiz
    """
    quiz = Quiz.objects.get(id=id)
    questions = Question.objects.filter(quiz=quiz)

    if request.method == 'POST':
        formset = EditQuestionModelFormSet(
            request.POST,
            queryset=questions
            )

        if formset.is_valid():

            for form in formset:
                if form.is_valid():
                    f = form.save(commit=False)
                    f.quiz = quiz
                    if Question.objects.filter(id=f.id).exists():
                        f.save()
                    else:
                        f.id = uuid.uuid4()
                        f.save()
                    
                else:
                    print("form is not valid")

            formset.save(commit=False)
            for object in formset.deleted_objects:
                object.delete()

            return redirect(reverse("quiz:index")) 

        else:
            print(formset.errors)
            return redirect(reverse("quiz:index")) 


    else:
        formset = EditQuestionModelFormSet(
            queryset=questions
            )

    return render(request, "quiz/edit-quiz.html", {
        "quiz":quiz,
        "formset": formset
    })


def play_quiz(request, id):
    """
    Play a quiz
    """
    quiz = Quiz.objects.get(id=id)
    questions = Question.objects.filter(quiz=quiz)

    if request.method == "POST":

        formset = PlayerAnswerModelFormSet(
            request.POST,
            queryset=questions
        )
        for form in formset:
            question = questions.get(question=form["question"].value())

            answer = PlayerAnswer(
                question=question,
                player_answer=form["player_answer"].value(),
                player=request.user
            )
            answer.save()            

        return redirect("quiz:quiz_result", id=quiz.id)
        
    else:
        formset = PlayerAnswerModelFormSet(
            queryset=questions
        )

        # Delete this
        for form in formset:
            q = questions.get(question=form["question"].value())

        return render(request, "quiz/play-quiz.html", {
            "quiz":quiz,
            "questions":questions,
            "formset":formset
        })


def quiz_result(request, id):
    """
    Return the results of a quiz to the player with correct answers
    """
    questions = Question.objects.filter(quiz=id)
    player_answers = PlayerAnswer.objects.filter(question__quiz=id).values("question", "player_answer", "correct")
    
    results=[]

    for question in questions:
        correct_answer = question.correct_answer
        player_answer_dict = player_answers.get(question = question.id)
        player_answer = player_answer_dict["player_answer"]
        correct = player_answer_dict["correct"]

        result = {
            "question":question.question,
            "correct_answer":correct_answer,
            "player_answer":player_answer,
            "correct": correct
        }

        results.append(result)

    return render(request, "quiz/quiz-result.html", {"results":results})

