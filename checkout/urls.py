from django.urls import path
from .views import (
        add_to_cart, 
        remove_from_cart, 
        CartItems, 
        remove_item_from_cart,
        add_to_cart_p,
        pre_checkout,
        pre_payment,
        host_to_host_callback,
)


app_name = 'checkout'

urlpatterns = [
        path('add_to_cart_p/', add_to_cart_p, name= 'add_to_cart_from_product'),
        path('add_to_cart/', add_to_cart, name= 'add_to_cart'),
        path('remove_from_cart/', remove_from_cart, name='remove_from_cart'),
        path('remove_item/', remove_item_from_cart, name='remove_item_from_cart'),
        path('cart', CartItems.as_view(), name='cart'),
        path('cart/checkout/', pre_checkout, name='pre_checkout'),
        path('cart/payment/request/', pre_payment, name='pre_payment'),
        path('payment/callback/', host_to_host_callback, name='h2h'),
    ]

