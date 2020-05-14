from django.shortcuts import render, redirect, reverse
from django.forms.models import model_to_dict
from django.conf import settings
from accounts.models import Profile, User
from quiz.models import Order
from .forms import PaymentDetailsForm
from cart.contexts import cart_contents
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import json
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY


# Create your views here.
@csrf_exempt
def checkout(request):
    """
    Payment page
    """
    if request.method == "POST":
        
        context = cart_contents(request)["cart_context"]
        user = User.objects.get(id=request.user.id)

        for product in context:
            quiz=product["product"]
            Order.objects.create(
                quiz=quiz.quiz,
                customer=request.user
            )

        subject = "Quizim Receipt"
        html_message = render_to_string("checkout/receipt-email.html", {"context":context})
        plain_message = strip_tags(html_message)
        from_email = settings.DEFAULT_FROM_EMAIL
        to = user.email
        mail.send_mail(subject, plain_message, from_email, [to,], html_message=html_message)
        
        del request.session["cart"]


        return redirect(reverse("checkout:payment_success"))

    else:
        user = User.objects.get(id=request.user.id)
        
        profile = Profile.objects.get(user=request.user)
        profile_dict = model_to_dict(profile)

        # Retrieving default data for PaymentDetails form will result in unnecessary data
        # retrieved from Profile model remove these fields before passing to 
        # PaymentDetailsForm. Also add card holder
        keys_to_remove = ["id", "user", "profile_pic", "email_confirmed", "receive_email"]
        for key in keys_to_remove:
            del profile_dict[key]
        
        default_cardholder = f'{profile.user.first_name} {profile.user.last_name}'
        profile_dict["cardholder"] = default_cardholder

        payment_details_form = PaymentDetailsForm(data=profile_dict)

        contents = cart_contents(request)
        amount = int(contents["total_price"] * 100)

        intent = stripe.PaymentIntent.create(
            amount=amount,
            currency="eur",
            payment_method_types=["card"]
        )   
        stripe_context = {
            "amount":intent.amount,
            "client_secret":intent.client_secret,
            "publishable":settings.STRIPE_PUBLISHABLE
        }

    return render(request, "checkout/checkout.html", {
        "stripe_context":stripe_context,
        "payment_details_form":payment_details_form
    })
        

def payment_success(request):
    """
    Display page on successful payment
    """
    return render(request, "checkout/payment-success.html")
