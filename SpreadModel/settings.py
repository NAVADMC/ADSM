"""
Django settings for SpreadModel project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import sys

if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '(iosdjsujy653@eo2lzs*x2$*OTGh#=y_vpzvbo6n^(7eao0-tbc!rcgd'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = (
    'ScenarioCreator',
    'Results',
    'ADSMSettings',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'floppyforms',
    'crispy_forms',
    'django_production_server',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'ADSMSettings.disable.DisableCSRF',
)

if DEBUG:
    MIDDLEWARE_CLASSES += (
        # 'ADSMSettings.debug.HotshotProfileMiddleware',
        # 'ADSMSettings.debug.cProfileMiddleware',
    )

ROOT_URLCONF = 'SpreadModel.urls'

WSGI_APPLICATION = 'SpreadModel.wsgi.application'

CRISPY_TEMPLATE_PACK = 'bootstrap'

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'NAME': os.path.join(BASE_DIR, 'settings.sqlite3'),
        'ENGINE': 'django.db.backends.sqlite3',
        'TEST_NAME': os.path.join(BASE_DIR, 'test_settings.sqlite3'),
    },
    'scenario_db': {
        'NAME': os.path.join(BASE_DIR, 'activeSession.sqlite3'),
        'ENGINE': 'django.db.backends.sqlite3',
        'TEST_NAME': os.path.join(BASE_DIR, 'test_activeSession.sqlite3'),
    }
}

DATABASE_ROUTERS = ['ScenarioCreator.router.ScenarioRouter', ]

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    # 'django.template.loaders.eggs.Loader',
)
TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    "django.core.context_processors.request",
    "ScenarioCreator.context_processor.basic_context",
    "Results.context_processor.results_context"

)
TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
)

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # 'django.contrib.staticfiles.finders.DefaultStorageFinder',
)
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'SpreadModel', 'static'),
)

from django.db.backends.signals import connection_created
from django.dispatch import receiver


@receiver(connection_created)
def activate_auto_vacuum(sender, connection, **kwargs):
    """Vacuum mode to keep file sizes reasonable with sqlite."""
    if connection.vendor == 'sqlite' or connection.vendor == 'sqlite3':
        cursor = connection.cursor()
        cursor.execute('PRAGMA auto_vacuum = FULL;')
#         cursor.execute('PRAGMA journal_mode = WAL;')