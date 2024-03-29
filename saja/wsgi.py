"""
WSGI config for saja project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/
"""

import os
from pathlib import Path

from django.core.wsgi import get_wsgi_application
from dotenv import load_dotenv

path = Path('../')
load_dotenv(dotenv_path=path)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "saja.settings.dev")

application = get_wsgi_application()
