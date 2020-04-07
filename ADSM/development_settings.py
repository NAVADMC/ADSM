import os
import sys


if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DB_BASE_DIR = None  # To have as 'settings' folder in WORKSPACE_PATH leave set to None

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'zkvb3#=7zub^kw-@hmf2v4rgsn%5q$!^0i4v#l)$_umn=_lx&3'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
TEMPLATE_DEBUG = DEBUG

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases
DATABASES = {

}

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

DEFAULT_FROM_EMAIL = 'noreply@development.server'  # Users get emails from this address 'info@mydomain.com'
SERVER_EMAIL = 'server@development.server'  # Admins and Managers get emails from this address about errors 'server@mydomain.com'