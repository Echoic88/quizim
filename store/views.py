from django.shortcuts import render
from quiz.models import PaidQuiz

# Create your views here.
def index(request):
    """
    Display main store page
    """
    quizes = PaidQuiz.objects.all() 
    return render(request, "store/index.html", {
        "quizes":quizes
    })