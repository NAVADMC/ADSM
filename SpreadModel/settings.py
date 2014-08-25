"""
Django settings for SpreadModel project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from future import standard_library
standard_library.install_hooks()

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from django.conf.global_settings import STATICFILES_DIRS

BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '(iosdjsujy653@eo2lzs*x2$*OTGh#=y_vpzvbo6n^(7eao0-tbc!rcgd'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True
# TEMPLATE_STRING_IF_INVALID = 'XXXXXX_BAD_{{ %s }}'

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'south',
    'floppyforms',
    'crispy_forms',
    'ScenarioCreator',
    'Results',
    'Settings',
    'django_production_server',
)
MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
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
    "ScenarioCreator.context_processor.basic_context"
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
        'USER': 'josiah',
        'PASSWORD': '1',
    },
    'scenario_db': {
        'NAME': os.path.join(BASE_DIR, 'activeSession.sqlite3'),
        'ENGINE': 'django.db.backends.sqlite3',
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


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/
STATIC_ROOT = BASE_DIR + '/static/'
STATICFILES_DIRS = (BASE_DIR + '/SpreadModel/static/', )
STATIC_URL = '/static/'

from django.db.backends.signals import connection_created
from django.dispatch import receiver


@receiver(connection_created)
def activate_write_ahead_mode(sender, connection, **kwargs):
    """Enable integrity constraint with sqlite."""
    if connection.vendor == 'sqlite' or connection.vendor == 'sqlite3':
        cursor = connection.cursor()
        cursor.execute('PRAGMA journal_mode = WAL;')