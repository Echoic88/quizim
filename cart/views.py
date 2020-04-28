from django.shortcuts import render, redirect, reverse, get_object_or_404
from quiz.models import PaidQuiz

# Create your views here.

def view_cart(request):
    """
    A View that renders the cart contents page
    """
    return render(request, "cart/cart.html")

    
def add_to_cart(request, id):
    """
    Add the specified product to the cart
    """
    # cart session data contains the ID of a PaidQuiz instance
    if request.session.get("cart") == None:
        cart = []
    else:
        cart = request.session["cart"]

    # Only add the quiz to the cart if it is not already
    # in there since quizes can only be bought once
    if id not in cart:
        cart.append(id)

    request.session["cart"] = cart
    return redirect(reverse("store:index"))


def remove_from_cart(request, id):
    """
    Remove an item from the cart
    """
    if request.session.get("cart") == None:
        cart = []
    else:
        cart = request.session["cart"]

    if id in cart:
        cart.remove(id)
    
    request.session["cart"] = cart
    return redirect(reverse("store:index"))
