from django import forms
from .models import Profile
from django_countries.widgets import CountrySelectWidget


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
        widgets = {"country":CountrySelectWidget()}
