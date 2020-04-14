import os
from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ['SECRET_KEY']

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ['*'] 

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# debug_toolbar
INSTALLED_APPS = INSTALLED_APPS + ['debug_toolbar']
MIDDLEWARE = MIDDLEWARE + [
        "debug_toolbar.middleware.DebugToolbarMiddleware",
]
INTERNAL_IPS = ("127.0.0.1", )


try:
    from .local import *
except ImportError:
    pass
