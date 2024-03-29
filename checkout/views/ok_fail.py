import hashlib
import html
import base64

from django.views.decorators.http import require_POST 
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.shortcuts import render
from django.conf import settings

from checkout.payment_request import postAuth_gen_hash
from checkout.models import Order
from checkout.tasks import send_invoice, send_order


@require_POST 
@csrf_exempt
def ok(request):
    # verify hash
    hash_dict = {k:html.unescape(v)  for k, v in request.POST.items() if k != "HASH" and k != "encoding"}
    calculated_hash = postAuth_gen_hash(hash_dict, settings.STORE_KEY)
    incoming_hash = base64.b64decode(request.POST.get('HASH'))
    oid = request.POST.get('oid')
    o = Order.objects.get(pk=int(oid))

    if calculated_hash == incoming_hash:
        o.user.carts.all()[0].delete()
        if o.status != Order.PAID:
            o.status = Order.PAID
            o.save()

    # send order emails
    send_order(o)
    send_invoice(o)

    return render(request, "checkout/payment_ok.html", {'order': o})


@require_POST
@csrf_exempt
def fail(request):
    oid = request.POST.get('oid')
    o = Order.objects.get(pk=int(oid))
    if o.status != Order.CANCELED:
        o.status = Order.CANCELED
        o.save()
    return render(request, "checkout/payment_fail.html", {'order': o})

