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
            'okUrl': 'https://sajacosmetics.com/payment/ok/',
            'failUrl': 'https://sajacosmetics.com/payment/fail/',
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
            'CallbackURL': 'https://sajacosmetics.com/payment/callback/',
            'shopurl': f'https://sajacosmetics.com/payment/{order.pk}/cancel/',
    }
    return req_attrs

