from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django_countries.widgets import CountrySelectWidget
from .models import Profile


class SignUpForm(UserCreationForm):
    
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields["email"].required = True



class ProfileForm(forms.ModelForm):
    
    class Meta:
        model = Profile
        fields = [
            "address1",
            "address2",
            "city",
            "postcode",
            "country",
            "profile_pic",
            "receive_email"
        ]
        
        widgets = {
            "country":CountrySelectWidget()
        }
        