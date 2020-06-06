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
            'okUrl': 'https://c5a154a3ebd5.ngrok.io/paymént/document/',#reverse('checkout:h2h')',
            'failUrl': 'https://c5a154a3ebd5.ngrok.io/payment/failUrl/',#reverse('checkout:h2h')',
            'lang': get_language()[:2],
            'email': customer.email,
            'BillToName': customer.get_full_name(),
            'tel': customer.address.phone,
            'BillToStreet1': customer.address.street,
            'BillToCity': customer.address.city,
            'rnd': order.rnd,
            'hashAlgorithm': 'ver3',
            'CallbackResponse': 'true',
            'AutoRedirect': 'true',
            'CallbackURL': 'http://c568dcfff1b1.ngrok.io/payment/callback/',#reverse('checkout:h2h'),
            'shopurl': f'http://c568dcfff1b1.ngrok.io/payment/{order.pk}/cancel/',#reverse('checkout:h2h')',
    }
    return req_attrs

