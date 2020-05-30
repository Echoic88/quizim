from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from accounts.models import Profile
from accounts.forms import ProfileForm
from quiz.models import Quiz, Question, PlayerAnswer, PlayedQuiz, Order
from .forms import UserUpdateForm

# Create your views here.
def index(request):
    """
    Return index.html for userarea
    """
    if request.user.is_authenticated:
        last_5_quizes = PlayedQuiz.objects.filter(player=request.user).order_by("-played_date")[:5]
        bar_chart_quiz_name = []
        bar_chart_quiz_score = []
        if last_5_quizes.exists():
            for quiz in last_5_quizes:
                bar_chart_quiz_name.append(quiz.quiz.quiz_name)
                bar_chart_quiz_score.append(quiz.score())

        bar_chart_data = {
            "bar_labels":bar_chart_quiz_name,
            "bar_series":bar_chart_quiz_score
        }

        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
        user_quizes = Quiz.objects.filter(creator=request.user)
        quizes_played = PlayedQuiz.objects.filter(player=request.user)
        quizes_purchased = Order.objects.filter(customer=request.user)

        password_form = PasswordChangeForm(request.user)
        
        context = {
            "user_form":user_form,
            "profile_form":profile_form,
            "user_quizes":user_quizes,
            "quizes_played":quizes_played,
            "quizes_purchased":quizes_purchased,
            "password_form":password_form,
            "bar_chart_data":bar_chart_data
        }

        return render(request, "userarea/index.html", context)

    else:
        messages.info(request, "Please log in to access the Userarea")
        return redirect(reverse("home:index"))




# @login_required
def update_user_details(request):
    """
    Form to update user details
    """
    if request.method =="POST":

        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileForm(
            request.POST, request.FILES, instance=request.user.profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect(reverse("userarea:index"))

        else:
            messages.error(request, user_form.errors)
            messages.error(request, profile_form.errors)

    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)

    return redirect(reverse("userarea:index"))


# from Simple Is Better Than Complex
# https://simpleisbetterthancomplex.com/tips/2016/08/04/django-tip-9-password-change-form.html
def change_password(request):
    if request.method == "POST":
        password_form = PasswordChangeForm(request.user, request.POST)
        if password_form.is_valid():
            user = password_form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Your password was successfully updated!")
            return redirect(reverse("userarea:index"))
        else:
            messages.error(request, "Please correct the error below.")
    else:
        password_form = PasswordChangeForm(request.user)
    return redirect(reverse("userarea:index"))
