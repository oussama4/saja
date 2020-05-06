from django.urls import path
from .views import (
        add_to_cart, 
        remove_from_cart, 
        CartItems, 
        remove_item_from_cart,
        add_to_cart_p,
)


app_name = 'checkout'

urlpatterns = [
        path('add_to_cart_p/', add_to_cart_p, name= 'add_to_cart_from_product'),
        path('add_to_cart/', add_to_cart, name= 'add_to_cart'),
        path('remove_from_cart/', remove_from_cart, name='remove_from_cart'),
        path('remove_item/', remove_item_from_cart, name='remove_item_from_cart'),
        path('cart', CartItems.as_view(), name='cart'),
    ]
