from io import BytesIO

import weasyprint

from django.template.loader import render_to_string
from django.core.mail import send_mail, EmailMessage
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.utils.html import strip_tags

from .models import Order

def send_invoice(order_id):
    """ sends an invoice mail to customer after a successful order """

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


def send_order(order_id):
    """ sends a notification email after a successful order """

    order = Order.objects.get(pk=order_id)

    # prepare mail
    subject = _(f"Sajacosmetics - Commande #{order.id}")
    message = _("une commande a été effectuée avec succès")
    email = EmailMessage(subject, message, settings.DEFAULT_FROM_EMAIL, [settings.SAJA_EMAIL])

    # generate pdf
    html_msg = render_to_string("checkout/invoice_pdf.html", {"order": order})
    buf = BytesIO()
    stylesheets = [weasyprint.CSS(settings.STATIC_ROOT + '/css/invoice.css')]
    weasyprint.HTML(string=html_msg).write_pdf(buf, stylesheets=stylesheets)

    email.attach(f'order_{order.id}.pdf', buf.getvalue(), 'application/pdf')
    email.send()

