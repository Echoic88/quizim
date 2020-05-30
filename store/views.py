from django.shortcuts import render, redirect, reverse
from quiz.models import PaidQuiz, Order
from django.contrib import messages

# Create your views here.
def index(request):
    """
    Display main store page
    """
    if request.user.is_authenticated:
        quizes = PaidQuiz.objects.all()
        previous_purchases = Order.objects.filter(customer=request.user)

        previous_purchases_list = []

        for quiz in quizes:
            for previous in previous_purchases:
                if previous.quiz == quiz.quiz:
                    previous_purchases_list.append(quiz)

        return render(request, "store/index.html", {
            "quizes":quizes,
            "previous_purchases_list":previous_purchases_list
        })

    else:
        messages.info(request, "Please log in to access the Store")
        return redirect(reverse("home:index"))
