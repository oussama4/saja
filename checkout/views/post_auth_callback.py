import hashlib
import html
import base64
import logging

from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import HttpResponse
from django.conf import settings

from checkout.payment_request import postAuth_gen_hash
from checkout.models import Order


logger = logging.getLogger('django')

@csrf_exempt
@require_POST
def host_to_host_callback(request):
    data = ""
    hash_dict = {k:html.unescape(v)  for k, v in request.POST.items() if k != "HASH" and k != "encoding"}
     
    try:
        order = Order.objects.get(pk=request.POST['oid'])
    except:
        order = None

    calculated_hash = postAuth_gen_hash(hash_dict, settings.STORE_KEY)
    incoming_hash = base64.b64decode(request.POST.get('HASH'))
    if calculated_hash == incoming_hash:
        if(str(request.POST['ProcReturnCode']) == '00'):
            order.status = Order.PAID
            order.save()
            data = "ACTION=POSTAUTH"
        else:
            data = "APPROVED"
    else:
        data = "FAILURE"
    logger.warning(data)
    return HttpResponse(data)

