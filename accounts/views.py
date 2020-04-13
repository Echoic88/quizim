from django.shortcuts import render, redirect, reverse
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.exceptions import ValidationError
from .forms import SignUpForm

# Create your views here.
def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)

        try:
            existing_user = User.objects.get(username=form["username"].value())
        except:
            existing_user = None
        
        if existing_user:
            messages.error(request, "This username is taken. Please choose another one")
            return redirect(reverse("accounts:signup"))

        else:
            if form.is_valid():
                f = form.save(commit=False)
                f.is_active = False
                f.save()
                return redirect(reverse("accounts:signup_success"))
        
            else:
                return redirect(reverse("home:index"))

        return redirect(reverse("home:index"))

    else:
        form = SignUpForm()
        
    return render(request, "accounts/signup.html", {
        "form":form
    })


def signup_success(request):
    """
    Display signup-success.html on successful registration
    """
    return render(request, "accounts/signup-success.html")
