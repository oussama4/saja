from django.contrib.auth.decorators import login_required 
from django.shortcuts import get_object_or_404
from .utils import memoize 
from .models import Cart, CartItem


def cart(request):

    if request.user.is_authenticated:
        
        cart= memoize(lambda:Cart.objects.prefetch_related('items').get_or_create(user_id=request.user))
        return {'cart':cart}

    return {}

