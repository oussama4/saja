from django.db import models
from django.core.validators import MaxValueValidator
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _
from django.utils.crypto import get_random_string

from users.models import User, Address


def total (items):
    total = 0
    for item in items:
        total+=item.total_price
    return total


class Cart(models.Model):

    user = models.ForeignKey(User, related_name="carts", on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)

    @property
    def total_price(self):
        return total(self.items.all())

    @property
    def total_quantity(self):
        tq = 0
        for item in self.items.all():
            tq+=item.quantity
        return tq
    @property
    def total_discount(self):
        td = 0
        for item in self.items.all():
            td+=item.item_discount
        return td

    @property
    def price_without_discount(self):
        return self.total_price+self.total_discount

    @property
    def is_empty(self):
        return self.items.count() == 0


class CartItem(models.Model):

    cart = models.ForeignKey(Cart, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey("catalog.Product" ,related_name="+", on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1,validators=[MaxValueValidator(10000)])
    created_date = models.DateTimeField(auto_now_add=True)

    @property
    def total_price(self):
        return self.quantity*self.product.price
    @property
    def item_discount(self):
        t =0
        if self.product.has_discount:
           t= (self.product.base_price*self.quantity)*self.product.discount_percent/100
        return t

    def __str__(self):
        return f"{self.quantity} x {self.product.title}"

class Order(models.Model):
    DELIVERED = "D"
    ONGOING = "O"
    PAID = "P"
    REFUND = "R"
    CANCELED = "C"
    order_status = [
            (PAID, 'Paid'),
            (DELIVERED, 'Delivered'),
            (ONGOING, 'Ongoing'),
            (REFUND, 'Refund'),
            (CANCELED, 'Canceled'),
        ]
    user = models.ForeignKey(User, related_name="orders", on_delete=models.PROTECT)
    status = models.CharField(max_length=2,
            choices=order_status,
            default=ONGOING
        )
    payment_date = models.DateTimeField(auto_now_add=True)
    shipping_address = models.ForeignKey(Address, related_name="+",on_delete=models.PROTECT)
    # random string, will be used for payment request hash comparaison
    rnd = models.CharField(max_length=20, default=get_random_string)

    class Meta:
        verbose_name = _("commande")
        verbose_name_plural = _("commandes")

    @property
    def total_price(self):
        return total(self.items.all())
    @property
    def delivered(self):
        self.status = self.Delivred
        self.save()
    @property
    def refund(self):
        self.status = self.Refund
        self.save()

class OrderItem(models.Model):

    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey("catalog.Product", related_name="+", on_delete=models.DO_NOTHING)
    quantity = models.IntegerField(default=1, validators=[MaxValueValidator(10000)])

    @property
    def total_price(self):
        return self.quantity * self.product.price

