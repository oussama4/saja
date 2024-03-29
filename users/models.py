from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.conf import settings
from django.urls import reverse

from .fields import MAPostalCodeField, PhoneNumberField

class Address(models.Model):
    line1 = models.CharField(
            verbose_name=_("adresse 1"),
            max_length=250,
            help_text=_("appartement, suite, unité, etc")
    )
    line2 = models.CharField(
            verbose_name=_("adresse 2"),
            max_length=250,
            help_text=_("adresse postale, boîte postale, etc")
    )
    postal_code = MAPostalCodeField(
            verbose_name=_("code postal"),
            help_text=_("code postal"),
            null=True,
            blank=True
    )
    city = models.CharField(
            verbose_name=_("ville"),
            help_text=_("ville"),
            max_length=64
    )
    phone = PhoneNumberField(
            verbose_name=_("numéro de téléphone"),
            help_text=_("numéro de téléphone")
    )

    class Meta:
        verbose_name = _("adresse")
        verbose_name_plural = _("adresses")

    def __str__(self):
        return f'{self.line1} \n {self.line2} \n {self.postal_code}  {self.city} \n {self.phone}'

    @property
    def street(self):
        return f'{self.line1} {self.line2}'


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
            max_length=64,
            verbose_name=_('adresse email'),
            unique=True,
            error_messages={
                'unique': _('Un utilisateur avec cet email existe déjà.')
            }
    )
    first_name = models.CharField(
            verbose_name=_('Prénom'), max_length=30
    )
    last_name = models.CharField(
            verbose_name=_('nom de famille'), max_length=30
    )
    is_staff = models.BooleanField(
        verbose_name=_('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        verbose_name=_('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(
            verbose_name=_('date joined'), default=timezone.now
    )
    address = models.ForeignKey(
            Address, related_name="+", null=True, blank=True, on_delete=models.SET_NULL
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        verbose_name = 'utilisateur'
        verbose_name_plural = 'utilisateurs'

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def get_absolute_url(self):
        return reverse('profile')

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

    @property
    def has_address(self):
        """ checks if a user has an address """

        if self.address:
            return True
        return False

    @property
    def has_name(self):
        """ checks if a user has a first_name and last_name """

        if self.first_name and self.last_name:
            return True
        return False

    @property
    def is_complete(self):
        """ checks if all nesseccery user information is provided """
        if self.has_address and self.has_name:
            return True
        return False

