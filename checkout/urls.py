from django.urls import path
from .views import add_to_cart, remove_from_cart, CartItems 


app_name = 'checkout'

urlpatterns = [
        path('add_to_cart/<int:id>/', add_to_cart, name= 'add_to_cart'),
        path('remove_from_cart/<int:id>', remove_from_cart, name='remove_from_cart'),
        path('cart', CartItems.as_view(), name='cart'),
    ]
