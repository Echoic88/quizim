from django.shortcuts import render, redirect, reverse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from accounts.models import Profile
from accounts.forms import ProfileForm

# Create your views here.
@login_required
def index(request):
    """
    Return index.html for userarea
    """
    profile_form = ProfileForm(instance=request.user.profile)
    return render(request, "userarea/index.html", {
        "profile_form":profile_form
    })


def update_user_details(request):
    """
    Form to update user details
    """
    if request.method =="POST":
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if profile_form.is_valid():
            profile_form.save()
            return redirect(reverse("userarea:index"))
        else:
            print(form.errors)
    else:
        profile_form = ProfileForm(instance=request.user.profile)

    return redirect(reverse("userarea:index"))
