from django.urls import path
from .views import index, update_user_details, change_password

app_name = "userarea"
urlpatterns = [
    path("", index, name="index"),
    path("update-details/", update_user_details, name="update_user_details"),
    path("change-password/", change_password, name="change_password"),
]