from django.shortcuts import render, redirect, reverse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from accounts.models import Profile
from accounts.forms import ProfileForm
from quiz.models import Quiz, Question, PlayerAnswer, PlayedQuiz
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

    context = {
        "user_form":user_form,
        "profile_form":profile_form,
        "user_quizes":user_quizes,
        "quizes_played":quizes_played
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
