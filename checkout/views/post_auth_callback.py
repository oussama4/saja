import hashlib
import html
import base64

from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import HttpResponse

from checkout.payment_request import postAuth_gen_hash
from checkout.models import Order



@csrf_exempt
@require_POST
def host_to_host_callback(request):
    print("this is callback {}".format(request.POST))
    data = ""
    hash_dict = {k:html.unescape(v)  for k, v in request.POST.items() if k != "HASH" and k != "encoding"}
     
    try:
        order = Order.objects.get(pk=request.POST['oid'])
    except:
        order = None

    calculated_hash = base64.b64encode(postAuth_gen_hash(hash_dict, settings.STORE_KEY))
    incoming_hash = request.POST.get('HASH')
    if calculated_hash == incoming_hash:
        if(str(request.POST['ProcReturnCode']) == '00'):
            order.status = Order.PAID
            order.save()
            data = "ACTION=POSTAUTH"
        else:
            data = "APPROVED"
    else:
        data = "FAILURE"
    print(data)
    return HttpResponse(data)

