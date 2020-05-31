from django.urls import path
from .views import checkout, payment_success

app_name = "checkout"
urlpatterns = [
    path("", checkout, name="checkout"),
    path("payment-success", payment_success, name="payment_success"),
]
