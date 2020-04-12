from django.shortcuts import render

# Create your views here.
def index(request):
    """
    Display home/index.html for the home page
    """
    return render(request, "home/index.html")