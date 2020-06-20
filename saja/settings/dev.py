import os
from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ['SECRET_KEY']

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ['*'] 

#EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# debug_toolbar
INSTALLED_APPS = INSTALLED_APPS + ['debug_toolbar','django_extensions','anymail', 'cookielaw']
MIDDLEWARE = MIDDLEWARE + [
        "debug_toolbar.middleware.DebugToolbarMiddleware",
]
INTERNAL_IPS = ("127.0.0.1", )
ANYMAIL = {
    "MAILGUN_API_KEY": config.get('MAILGUN_API_KEY'),
    "MAILGUN_SENDER_DOMAIN": 'mail.sajacosmetics.com',
}
EMAIL_BACKEND = "anymail.backends.mailgun.EmailBackend"
DEFAULT_FROM_EMAIL = "admin@sajacosmetics.com"
SAJA_EMAIL = 'oussamazouaki4@gmail.com'

STORE_KEY = "Codylia2020"


try:
    from .local import *
except ImportError:
    pass
