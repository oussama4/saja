from django.conf import settings
from django.urls import reverse
from django.utils.translation import get_language
from django.utils.timezone import now

def payment_request_attributes(order, request):
    req_attrs = {
            'clientid': settings.CLIENT_ID,
            'storetype': settings.STORE_TYPE,
            'trantype': settings.TRANTYPE,
            'amount': str(order.total_price),
            'currency': "504",
            'oid': str(order.pk),
            'okUrl': request.build_absolute_uri("/payment/ok/"), #'http://localhost:8000/payment/ok/',
            'failUrl': request.build_absolute_uri("/payment/fail/"),  #'http://localhost:8000/payment/fail/',
            'lang': get_language()[:2],
            'email': request.user.email,
            'BillToName': request.user.get_full_name(),
            'tel': request.user.address.phone,
            'BillToStreet1': request.user.address.street,
            'BillToCity': request.user.address.city,
            'rnd': order.rnd,
            'hashAlgorithm': 'ver3',
            'CallbackResponse': 'true',
            'AutoRedirect': 'true',
            'CallbackURL': request.build_absolute_uri("/payment/callback/"), #'http://localhost:8000/payment/callback/',
            'shopurl': request.build_absolute_uri(f"/payment/{order.pk}/cancel/"),
    }
    return req_attrs

