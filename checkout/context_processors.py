from django.contrib.auth.decorators import login_required 
from django.shortcuts import get_object_or_404

from .models import Cart, CartItem


def cart(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.prefetch_related('items').get_or_create(user_id=request.user)
        if cart and not created:
            return {'cart':cart}

    return {}

