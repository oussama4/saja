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
            'okUrl': 'http://75de5aec439a.ngrok.io/payment/ok/',#reverse('checkout:h2h')',
            'failUrl': 'http://75de5aec439a.ngrok.io/payment/fail/',#reverse('checkout:h2h')',
            'lang': get_language()[:2],
            'email': customer.email,
            'BillToName': customer.get_full_name(),
            'rnd': order.rnd,
            'hashAlgorithm': 'ver3',
            'CallbackResponse': 'true',
            'CallbackURL': 'http://75de5aec439a.ngrok.io/payment/callback/',#reverse('checkout:h2h'),
            'shopurl': 'localhost:8000',
    }
    return req_attrs

