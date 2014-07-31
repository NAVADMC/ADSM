"""
WSGI config for SpreadModel project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from future import standard_library
standard_library.install_hooks()

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SpreadModel.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
