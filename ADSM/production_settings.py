import os
import sys


if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
    if BASE_DIR.endswith('bin'):
        BASE_DIR = os.path.dirname(BASE_DIR)
else:
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

WORKSPACE_PATH = None  # To detect automatically or use settings from installer, set to None

DB_BASE_DIR = None  # To have as 'settings' folder in WORKSPACE_PATH leave set to None

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '%8d=)6kvtzwg0uyu+o&tuk4!)nioh&zuu1#+fpdxz=&9rkl^%y'  # TODO: Change this in a Cloud Environment!

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
TEMPLATE_DEBUG = DEBUG

# If not a subdomain, you need the www version and bare version ['www.mydomain.com', 'mydomain.com']
# If on a subdomain, you just need the one entry ['subdomain.mydomain.com', ]
ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases
DATABASES = {

}

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)  # These get error emails

MANAGERS = (
    # ('Your Name', 'your_email@example.com'),
)  # These guys get emails about broken links.

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

DEFAULT_FROM_EMAIL = 'noreply@development.server'  # Users get emails from this address 'info@mydomain.com'
SERVER_EMAIL = 'server@development.server'  # Admins and Managers get emails from this address about errors 'server@mydomain.com'

os.environ['HTTPS'] = 'off'
os.environ['wsgi.url_scheme'] = 'http'

SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
SESSION_EXPIRE_AT_BROWSER_CLOSE = False