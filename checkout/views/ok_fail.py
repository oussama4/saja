from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.shortcuts import render

from checkout.models import Order


@csrf_exempt
def ok(request):
    oid = request.POST.get('oid')
    u = request.user
    u.carts.all()[0].delete()
    o = Order.objects.get(pk=int(oid))
    return render(request, "checkout/payment_ok.html", {'order': o})

@csrf_exempt
def fail(request):
    #oid = request.POST.get('oid')
    o = Order.objects.get(pk=28)
    return render(request, "checkout/payment_fail.html", {'order': o})

