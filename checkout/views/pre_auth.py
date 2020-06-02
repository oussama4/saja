from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from checkout.create_order import create_order
from checkout.payment_req_attr import payment_request_attributes
from checkout.payment_request import generateHash


@login_required
def pre_payment(request):
    """ sends a hidden payment request form template """

    o = create_order(request.user)
    a = payment_request_attributes(o, request.user)
    at = generateHash(a, 'Codylia2020')
    return render(request, "checkout/preAuth.html", {'attrs': at})
