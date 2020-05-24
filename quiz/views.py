from django.shortcuts import render, redirect, reverse
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.template.loader import render_to_string
from accounts.models import Profile
from .forms import QuizForm, CreateQuestionModelFormSet, EditQuestionModelFormSet, PlayerAnswerModelFormSet
from .models import Question, Quiz, PlayerAnswer, PlayedQuiz
import uuid

# Create your views here.

def index(request):
    """
    Temporary home page for testing quiz links
    """
    last_three_user_quizes = Quiz.objects.filter(creator=request.user).order_by("-created_date")[:3]
    non_user_quizes = Quiz.objects.exclude(creator=request.user)
    question_man_list = []
    for i in range(4):
        question_man_list.append("images/question-man{0}.png".format(i))

    return render(request, "quiz/index.html", {
        "question_man_list":question_man_list,
        "quizes":non_user_quizes,
        "user_quizes":last_three_user_quizes
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
            q.id = uuid.uuid4()
            q.creator = request.user
            q.save()

        if questions_formset.is_valid():
            for form in questions_formset:
                f = form.save(commit=False)
                f.id = uuid.uuid4()
                f.quiz = q
                f.save()

        mailing_list = []
        people_to_email = Profile.objects.filter(receive_email=True)
        current_site = get_current_site(request)
        subject = "New Quiz!"
        quiz_maker = request.user.username
        from_mail="quizm4project@gmail.com"
        message = render_to_string("quiz/new-quiz-email.html", {
            "domain": current_site.domain,
            "quiz_maker":quiz_maker,
            "quiz_id":q.id
        })

        for person in people_to_email:
            recipient_name = "{0} {1}".format(person.user.first_name, person.user.last_name)
            recipient_email = person.user.email
            send_mail(subject, message, from_mail, [recipient_email,])

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
        try:
            formset = PlayerAnswerModelFormSet(
                request.POST,
                queryset=questions
            )
            for form in formset:
                # No check for form validation here since although the queryset
                # is of Question instances these are not modified and saved.
                # An instance of PlayerAnswer is created and saved for each form
                question = questions.get(question=form["question"].value())

                answer = PlayerAnswer(
                    question=question,
                    player_answer=form["player_answer"].value(),
                    quiz=quiz,
                    player=request.user
                )
                answer.save()

            PlayedQuiz.objects.create(
                quiz=quiz,
                player=request.user
            )

            # Update the counter for instances of this quiz played 
            quiz.instances_played += 1
            quiz.save()

            return redirect("quiz:quiz_result", id=quiz.id)

        except:
            print("Error saving Player Answers and Played Quiz")
            
    else:
        formset = PlayerAnswerModelFormSet(
            queryset=questions
        )

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
    player_answers = PlayerAnswer.objects.filter(player=request.user, question__quiz=id).values("question", "player_answer", "correct")
    
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
