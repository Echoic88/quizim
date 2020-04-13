from django.urls import path
from .views import signup, signup_success

app_name = "accounts"
urlpatterns = [
    path("signup/", signup, name="signup"),
    path("signup-success/", signup_success, name="signup_success"),
]
