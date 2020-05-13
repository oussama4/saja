from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.utils.html import strip_tags

from .models import Order

def send_invoice(order_id):
    """ sends an invoice mail after a successful order """

    order = Order.objects.get(pk=order_id)

    # prepare invoice e-mail
    subject = _(f"Sajacosmetics - Facture #{order.id}")
    html_msg = render_to_string("checkout/invoice.html", {"order": order})

    send_mail(
            subject,
            strip_tags(html_msg),
            settings.DEFAULT_FROM_EMAIL,
            [order.user.email],
            html_message=html_msg
    )

