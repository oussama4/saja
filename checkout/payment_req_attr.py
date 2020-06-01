from django.conf import settings
from django.urls import reverse
from django.utils.translation import get_language
from django.utils.timezone import now

def payment_request_attributes(order, customer):
    req_attrs = {
            'clientid': settings.CLIENT_ID,
            'storetype': settings.STORE_TYPE,
            'trantype': settings.TRANTYPE,
            'amount': str(order.total_price),
            'currency': "504",
            'oid': str(order.pk),
            'okUrl': '/',
            'failUrl': '/',
            'lang': get_language(),
            'email': customer.email,
            'BillToName': customer.get_full_name(),
            'rnd': str(now()),
            'hashAlgorithm': 'ver3',
            'encoding': 'utf-8',
    }
    return req_attrs

