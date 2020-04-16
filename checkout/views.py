from django.shortcuts import render, redirect , get_object_or_404 
from django.http import JsonResponse
from wagtail.images.models import Image 
from wagtail.images.views.serve import generate_image_url
from .models import Cart, CartItem
from catalog.models import product 
# Create your views here.

def add_to_cart(request, id):
    item = get_object_or_404(product.Product, page_ptr_id=id)
    cart, created = Cart.objects.get_or_create(
            user_id = request.user,
    )
    cart_item, create = CartItem.objects.get_or_create(
        cart_id = cart,
        product_id = item,
    )
    if not create:
        cart_item.quantity = int(cart_item.quantity) + 1
        cart_item.save()
    if cart_item:
        image =str(generate_image_url(cart_item.product_id.first_image.product_image,'fill-200x150'))
        cartItems={}
        cartItems['product'] = [cart_item.product_id.title,image,cart_item.product_id.price,cart_item.quantity]
    
    return JsonResponse(cartItems)
