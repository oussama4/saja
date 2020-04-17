from django.shortcuts import render, redirect , get_object_or_404 
from django.contrib import messages
from django.http import JsonResponse 
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, View 
from django.contrib.auth.mixins import LoginRequiredMixin

from wagtail.images.models import Image 
from wagtail.images.views.serve import generate_image_url

from .models import Cart, CartItem
from catalog.models import product 
# Create your views here.

@login_required
def add_to_cart(request, id):
    item = get_object_or_404(product.Product, page_ptr_id=id)
    cart, created = Cart.objects.get_or_create(
            user_id = request.user,
    )
    cart_item, create = CartItem.objects.get_or_create(
        cart_id = cart,
        product_id = item,
    )

    cartItems = {}
    if not create:
        cart_item.quantity = int(cart_item.quantity) + 1
        cart_item.save()
        cartItems['product'] = [str(cart_item.product_id.page_ptr_id),str(cart_item.quantity)]
        cartItems['existe'] = True
        print(cartItems)
    if create:
        try:
            image =str(generate_image_url(cart_item.product_id.first_image.product_image,'fill-200x150'))
        except AttributeError:
            image = '/static/img/images.png'

        cartItems['product']= [cart_item.product_id.title,image,cart_item.product_id.price,cart_item.quantity]
        cartItems['existe'] = False
        
    cartItems['total'] = cart.total_price
        
    return JsonResponse(cartItems)


@login_required
def remove_from_cart(request, id):
    item = get_object_or_404(product.Product, page_ptr_id=id)
    cart = Cart.objects.get(user_id = request.user)

    cart_item = CartItem.objects.get(cart_id = cart,product_id = item)
    print(cart_item)
    itemDelete = {}
    if cart_item:
        cart_item.delete()
        itemDelete['delete'] = True
        itemDelete['quantity'] = cart_item.quantity 
    else:
        itemDelete['delete'] = False 
    if cart:
        itemDelete['total'] = cart.total_price 
    
    return JsonResponse(itemDelete)

@login_required
def cartItems(request):
    cart = get_object_or_404(Cart, user_id= request.user)
    queryset = list(cart.items.all())
    return render(request)

class CartItems(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            cart = Cart.objects.get(user_id=self.request.user)
            context = {
                'object': cart 
            }
            return render(self.request, 'checkout/cart.html', context)
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active cart")
            return redirect("/")
