import os
from .base import *

DEBUG = False

ALLOWED_HOSTS = ['*']

SECRET_KEY = config.get('SECRET_KEY')
#SECURE_CONTENT_TYPE_NOSNIFF = True
#SECURE_BROWSER_XSS_FILTER = True
#SECURE_SSL_REDIRECT = True
#X_FRAME_OPTIONS = 'DENY'
#USE_X_FORWARDED_HOST = True

CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True

# email
EMAIL_HOST = 'smtp.zoho.com'
EMAIL_PORT = 465
EMAIL_USE_SSL = True
DEFAULT_FROM_EMAIL = 'admin@sajacosmetics.com'
EMAIL_HOST_USER = 'admin@sajacosmetics.com'
EMAIL_HOST_PASSWORD = 'Y5LBgSPcjACt'

try:
    from .local import *
except ImportError:
    pass
