from django.shortcuts import get_object_or_404
from quiz.models import PaidQuiz

def cart_contents(request):
    """
    Cart can be accessed from any page
    """
    cart_context=[]
    try:
        cart_contents = request.session.get("cart")
        for id in cart_contents:
            product = get_object_or_404(PaidQuiz, pk=id)
            cart_context.append({"id":id, "product":product})

    except:
        cart_context = []
    
    return {"cart_context": cart_context}
