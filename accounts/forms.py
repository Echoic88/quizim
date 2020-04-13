from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django_countries.widgets import CountrySelectWidget
from .models import Profile


class SignUpForm(UserCreationForm):
    
    class Meta:
        model = User
        fields = ["username", "password1", "password2"]


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
        labels = {
            "profile_pic":"Profile Picture (JPEG or PNG)"
        }
        widgets = {
            "country":CountrySelectWidget()
        }
