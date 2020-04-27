import os
from .base import *

DEBUG = False

ALLOWED_HOSTS = ['.sajacosmetics.com']

INSTALLED_APPS = INSTALLED_APPS + ['anymail']

SECRET_KEY = config.get('SECRET_KEY')
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_SSL_REDIRECT = True
X_FRAME_OPTIONS = 'DENY'
USE_X_FORWARDED_HOST = True

CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True

# email
ANYMAIL = {
    "MAILGUN_API_KEY": config.get('MAILGUN_API_KEY'),
    "MAILGUN_SENDER_DOMAIN": 'mail.sajacosmetics.com',
}
EMAIL_BACKEND = "anymail.backends.mailgun.EmailBackend"
DEFAULT_FROM_EMAIL = "osama@sajacosmetics.com"


#EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
#EMAIL_HOST = 'smtp.zoho.com'
#EMAIL_PORT = 465
#EMAIL_USE_SSL = True
#DEFAULT_FROM_EMAIL = 'admin@sajacosmetics.com'
#EMAIL_HOST_USER = 'admin@sajacosmetics.com'
#EMAIL_HOST_PASSWORD = 'Y5LBgSPcjACt'

# logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'filters': ['require_debug_false'],
            'class': 'logging.FileHandler',
            'filename': '/home/codylia/saja_app.log',
        }
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
        }
    }
}

SITE_ID = 2

try:
    from .local import *
except ImportError:
    pass
