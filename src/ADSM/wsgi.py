"""
WSGI config for ADSM project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""

import os
import sys


if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.join(os.path.dirname(sys.executable), 'src')
else:
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

sys.path.append(os.path.dirname(BASE_DIR))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ADSM.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
