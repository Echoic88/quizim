from django.shortcuts import render, redirect, reverse
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import send_mail, EmailMessage
from .forms import SignUpForm
from .tokens import account_activation_token


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

        try:
            existing_email = User.objects.get(email=form["email"].value())
        except:
            existing_email = None
        
        if existing_email:
            messages.error(request, "This email address is taken. Please choose another one")
            return redirect(reverse("accounts:signup"))

        else:
            # Modified from Simple Is Better Than Complex
            # https://simpleisbetterthancomplex.com/tutorial/2017/02/18/how-to-create-user-sign-up-view.html#sign-up-with-confirmation-mail
            if form.is_valid():
                try:
                    user = form.save(commit=False)
                    user.is_active = False
                    user.save()
                    current_site = get_current_site(request)
                    subject = "Complete registration for your Quizim account"
                    message = render_to_string("accounts/signup-activate-email.html", {
                        "user": user,
                        "domain": current_site.domain,
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "token": account_activation_token.make_token(user),
                    })
                    user.email_user(subject, message, from_email="quizm4project@gmail.com")

                    return redirect(reverse("accounts:signup_pending"))

                except:
                    print("Error saving user and send confirmation email")
        
            else:
                messages.error(request, "Invalid Form. Please try again")
                return redirect(reverse("accounts:signup"))

    else:
        form = SignUpForm()
        
    return render(request, "accounts/signup.html", {
        "form":form
    })


def signup_pending(request):
    """
    Display the signup-pending.html
    """
    return render(request, "accounts/signup-pending.html")


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        login(request, user)
        return render(request, "accounts/signup-success.html", {
            "user":user
        })
    else:
        return render(request, "accounts/signup-activation-invalid.html")


def signin(request):
    # From CI Lesson
    """
    log in user
    """
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
    
        if not user is None:
            login(request, user)
            messages.success(request, f"Hi {user.username}")
            return redirect(reverse("home:index"))

        else:
            messages.error(request, "Incorrect username or password. Please try again or register")
            return redirect(reverse("home:index"))

    else:
        return redirect(reverse("home:index"))


def signout(request):
    """
    log out user
    """
    logout(request)
    return redirect(reverse("home:index"))
