from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django_countries.fields import CountryField
from django_countries import countries
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver


# Create your models here.

class Profile(models.Model):
    """
    Model for user profile/personal details
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address1 = models.CharField(max_length=100, blank=True)
    address2 = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    postcode = models.CharField(max_length=10, blank=True)
    country = CountryField(null=True, blank=True)
    profile_pic = models.ImageField(
        upload_to="profile_pictures",
        null=True,
        blank=True,
        max_length=100
    )
    email_confirmed = models.BooleanField(default=False)
    receive_email = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    def clean(self): 
        if len(self.address1) > 100:
            raise ValidationError("Max length is 100 characters", code="field_too_long")
        if len(self.address2) > 100:
            raise ValidationError("Max length is 100 characters", code="field_too_long")
        if len(self.city) > 100:
            raise ValidationError("Max length is 100 characters", code="field_too_long")
        if len(self.postcode) > 10:
            raise ValidationError("Max length is 10 characters.", code="field_too_long")

        # Raise validation error if the country submitted is not a valid
        # country in django_countries package
        if self.country:
            test_list = []
            for country in countries:
                # extract the country name from tuples
                test_list.append(country[0].lower())
            if str(self.country).lower() not in test_list:
                raise ValidationError("This is not a valid country", code="invalid_country")


# from Simple Is Better Than Complex
# https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html#onetoone
# Create a Profile instance along when a User instance is created
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


# Modified from Stack Overflow
# https://stackoverflow.com/questions/19287719/remove-previous-image-from-media-folder-when-imagefiled-entry-modified-in-django
@receiver(pre_save, sender=Profile)
def delete_old_image(sender, instance, *args, **kwargs):
    if instance.pk:
        existing_image = Profile.objects.get(pk=instance.pk)
        if instance.profile_pic and existing_image.profile_pic != instance.profile_pic:
            existing_image.profile_pic.delete(False)
