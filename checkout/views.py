from django.shortcuts import render, redirect , get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, View
from django.contrib.auth.mixins import LoginRequiredMixin

from wagtail.images.models import Image
from wagtail.images.views.serve import generate_image_url

from catalog.models import Product
from .models import Cart, CartItem


@login_required
def add_to_cart(request):
    quantityF = request.POST.get('quantity')
    productID = request.POST.get('product')
    id = request.POST.get("id")
    if productID and quantityF:
        item = get_object_or_404(Product, pk=productID)
        cart , created = Cart.objects.get_or_create(
                user = request.user,
        )
        cart_item, create = CartItem.objects.select_related('product').get_or_create(
                cart = cart,
                product = item,
        )
        if create and int(quantityF > 0):
            cart_item.quantity = int(quantityF) 
            cart_item.save()
        elif not create and cart_item:
            cart_item.quantity += int(quantityF) 
            cart_item.save()
        return redirect('/cart/')
    elif request.method == "POST" and id :
        item = get_object_or_404(Product, pk=id)
        cart, created = Cart.objects.get_or_create(
                user = request.user,
        )
        cart_item, create = CartItem.objects.select_related('product').get_or_create(
            cart = cart,
            product = item,
        )

        cartItems = {}
        if not create:
            cart_item.quantity = int(cart_item.quantity) + 1
            cart_item.save()
            cartItems['product'] = [str(cart_item.product.id), str(cart_item.quantity)]
            cartItems['existe'] = True
        if create:
            try:
                image =str(generate_image_url(cart_item.product.first_image.product_image,'fill-200x150'))
            except AttributeError:
                image = '/static/img/images.png'

            cartItems['product']= [cart_item.product.title, image, cart_item.product.price, cart_item.quantity]
            cartItems['existe'] = False

        cartItems['total'] = cart.total_price
        cartItems['totalItem'] = cart_item.total_price
        cartItems['discount']  = cart.total_discount
        cartItems['totalDiscount'] = cart.price_without_discount
        return JsonResponse(cartItems)


@login_required
def remove_from_cart(request):
    if request.method == "POST":
        id = request.POST.get("id")
        item = get_object_or_404(Product, pk=id)
        cart = Cart.objects.get(user = request.user)

        cart_item = CartItem.objects.select_related('product').get(cart = cart, product = item)
        itemDelete = {}
        if cart_item:
            cart_item.delete()
            itemDelete['delete'] = True
            itemDelete['quantity'] = cart_item.quantity 
        else:
            itemDelete['delete'] = False 
        if cart:
            itemDelete['total'] = cart.total_price 
        itemDelete['discount']  = cart.total_discount 
        itemDelete['totalDiscount'] = cart.price_without_discount 
        return JsonResponse(itemDelete)

@login_required
def remove_item_from_cart(request):
    if request.method == "POST":
        id = request.POST.get("id")
        item = get_object_or_404(Product, pk=id)
        cart = Cart.objects.get(user = request.user)

        cart_item = CartItem.objects.select_related('product').get(cart = cart, product = item)
        itemRemove = {}
        if cart_item:
            if cart_item.quantity > 1:
                cart_item.quantity-=1
                cart_item.save()
                itemRemove['quantity']=cart_item.quantity
                itemRemove['totalItem'] = cart_item.total_price
                itemRemove['delete'] = False
            elif cart_item.quantity <= 1:
                cart_item.delete()
                cart_item['delete'] = True
        if cart:
            itemRemove['total'] = cart.total_price
            itemRemove['discount']  = cart.total_discount
            itemRemove['totalDiscount'] = cart.price_without_discount 
        return JsonResponse(itemRemove)


class CartItems(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
       # try:
       #     cart = Cart.objects.prefetch_related('items').get(user=self.request.user)
       #     context = {
       #         'object': cart,
       #         'discount':cart.price_without_discount  
       #     }
        return render(self.request, 'checkout/cart.html')
       # except ObjectDoesNotExist:
       #     messages.warning(self.request, "You do not have an active cart")
       #     return redirect("/")
