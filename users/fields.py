from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator


class MAPostalCodeField(models.CharField):

    default_validators = [RegexValidator(r'^\d{5}$', _("Invalid postal code"))]
    description = _("Postal code")

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 5
        super().__init__(*args, **kwargs)


class PhoneNumberField(models.CharField):
    default_validators = [RegexValidator(r'^(\+|0)?([0-9]){6,13}$', _("Invalid phone number"))]
    description = _("Phone number")

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 40
        super().__init__(*args, **kwargs)

