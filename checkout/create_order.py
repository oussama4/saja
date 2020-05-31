from django.db import DatabaseError

from .models import Order, OrderItem


def create_order(user):
    """ create an order from a cart model """

    try:
        o = Order.objects.create(user=user, status=Order.Pending, shipping_address=user.address)
        cart = user.carts.all()[0]
        for item in cart.items.all():
            order_item = OrderItem.objects.create(order=o, product=item.product, quantity=item.quantity)
    except DatabaseError as err:
        raise err
    finally:
        return o

