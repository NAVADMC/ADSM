"""
Django settings for ADSM project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(ADSM_DIR, ...)
import os
import sys


PRODUCTION_SETTINGS = False  # When you want to enable the production settings, copy the template file and modify
OVERRIDE_DEBUG = False
if PRODUCTION_SETTINGS:
    PRODUCTION_SETTINGS = True
    from ADSM.production_settings import *
else:
    PRODUCTION_SETTINGS = False
    from ADSM.development_settings import *
if OVERRIDE_DEBUG:
    DEBUG = True
    TEMPLATE_DEBUG = DEBUG

    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

    os.environ['HTTPS'] = 'off'
    os.environ['wsgi.url_scheme'] = 'http'
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False

# Look for any settings to import from the installer
if os.path.isfile(os.path.join(BASE_DIR, 'settings.ini')):
    from importlib import machinery
    install_settings = machinery.SourceFileLoader('install_settings', os.path.join(BASE_DIR, 'settings.ini')).load_module()
    WORKSPACE_PATH = install_settings.WORKSPACE_PATH

INSTALLED_APPS = (
    'ScenarioCreator',
    'Results',
    'ADSMSettings',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.humanize',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'floppyforms',
    'crispy_forms',
    'productionserver',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'ADSMSettings.disable.DisableCSRF',  # TODO: This needs to be fixed before we do a cloud deployment!
    # TODO: Add in the django.middleware.security.SecurityMiddleware
)

if DEBUG:
    MIDDLEWARE_CLASSES += (
        # 'ADSMSettings.debug.HotshotProfileMiddleware',
        # 'ADSMSettings.debug.cProfileMiddleware',
    )

ROOT_URLCONF = 'ADSM.urls'

WSGI_APPLICATION = 'ADSM.wsgi.application'

CRISPY_TEMPLATE_PACK = 'bootstrap'

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases


DATABASES.update({
    'default': {
        'NAME': os.path.join(DB_BASE_DIR, 'settings.sqlite3'),
        'ENGINE': 'django.db.backends.sqlite3',
        'TEST': {'NAME': os.path.join(DB_BASE_DIR, 'test_settings.sqlite3')},
    },
    'scenario_db': {
        'NAME': os.path.join(DB_BASE_DIR, 'activeSession.sqlite3'),
        'ENGINE': 'django.db.backends.sqlite3',
        'TEST': {'NAME': os.path.join(DB_BASE_DIR, 'test_activeSession.sqlite3')},
        'OPTIONS': {
            'timeout': 300,
        }
    }
})

DATABASE_ROUTERS = ['ScenarioCreator.router.ScenarioRouter', ]

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = False

USE_L10N = True

USE_TZ = True

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    # 'django.template.loaders.eggs.Loader',
)
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [

        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                "django.contrib.auth.context_processors.auth",
                "django.core.context_processors.debug",
                "django.core.context_processors.i18n",
                "django.core.context_processors.media",
                "django.core.context_processors.static",
                "django.core.context_processors.tz",
                "django.contrib.messages.context_processors.messages",
                "django.core.context_processors.request",
                "ADSMSettings.context_processor.adsm_context",
                "ScenarioCreator.context_processor.basic_context",
                "Results.context_processor.results_context"
            ],
        },
    },
]
if getattr(sys, 'frozen', False):
    for app_name in INSTALLED_APPS:
        if os.path.exists(os.path.join(BASE_DIR, 'templates', app_name)):
            TEMPLATES[0]['DIRS'].extend([os.path.join(BASE_DIR, 'templates', app_name), ])

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
    os.path.join(BASE_DIR, 'ADSM', 'static'),
)

LOGIN_REDIRECT_URL = '/'

LOCALE_PATHS = ()
if getattr(sys, 'frozen', False):
    for app_name in INSTALLED_APPS:
        if os.path.exists(os.path.join(BASE_DIR, 'locale', app_name)):
            LOCALE_PATHS += (os.path.join(BASE_DIR, 'locale', app_name), )
