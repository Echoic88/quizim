from django.contrib.auth.forms import AuthenticationForm

def sitewide_login_form(request):
    login_form = AuthenticationForm()
    return {"login_form":login_form}
