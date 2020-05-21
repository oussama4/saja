import os
from .base import *

DEBUG = False

ALLOWED_HOSTS = ['.sajacosmetics.com']

INSTALLED_APPS = INSTALLED_APPS + ['anymail','storages','cookielaw']

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
DEFAULT_FROM_EMAIL = "admin@sajacosmetics.com"
SAJA_EMAIL = 'safae@sajacosmetics.com'

# logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
    },
    'formatters': {
        'saja': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        }
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'filters': ['require_debug_false'],
            'class': 'logging.FileHandler',
            'filename': '/home/codylia/saja_app.log',
	    'formatter': 'saja',
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
#Object_storage_settings
AWS_ACCESS_KEY_ID = config.get('OBJECT_STORAGE_ACCESS_KEY')
AWS_SECRET_ACCESS_KEY = config.get('OBJECT_STORAGE_SECRET_KEY')
AWS_STORAGE_BUCKET_NAME= 'saja-bucket-1'
AWS_S3_OBJECT_PARAMETERS = {
            'CacheControl': 'max-age=86400',
#            'Access-Control-Allow-Origin': '*',
            }
AWS_DEFAULT_ACL = None
AWS_S3_FILE_OVERWRITE = True
AWS_LOCATION = 'static'
AWS_S3_ENDPOINT_URL  = "https://eu-central-1.linodeobjects.com"
STATIC_URL = f'https://{AWS_S3_ENDPOINT_URL}/'
STATIC_ROOT = f'https://{AWS_S3_ENDPOINT_URL}/'
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

MEDIAFILES_LOCATION = 'media'
MEDIA_URL = f'https://{AWS_S3_ENDPOINT_URL}/{MEDIAFILES_LOCATION}/'
DEFAULT_FILE_STORAGE = 'saja.settings.storage_backends.MediaStorage'


try:
    from .local import *
except ImportError:
    pass
