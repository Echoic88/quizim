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
@login_required
def index(request):
    """
    Return index.html for userarea
    """
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
    }

    return render(request, "userarea/index.html", context)


def update_user_details(request):
    """
    Form to update user details
    """
    if request.method =="POST":

        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect(reverse("userarea:index"))

        else:
            print(user_form.errors)
            print(profile_form.errors)

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
