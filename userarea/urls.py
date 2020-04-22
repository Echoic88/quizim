from django.urls import path
from .views import index, update_user_details

app_name = "userarea"
urlpatterns = [
    path("", index, name="index"),
    path("update-details", update_user_details, name="update_user_details"),
]