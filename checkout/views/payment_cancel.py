from django.shortcuts import render

from checkout.models import Order

def payment_cancel(request, oid):
    o = Order.objects.get(pk=oid)
    o.status = Order.CANCELED
    o.save()
    o.user.carts.all()[0].delete()
    return render(request, "checkout/payment_cancel.html", {'order': o})

