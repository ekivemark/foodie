#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4

import os
import sys
import tempfile

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
APPS_DIR = os.path.join(BASE_DIR, 'apps')
sys.path.insert(0, APPS_DIR)

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Mark Scirmshire', 'mark+foodie@HealthCa.mp'),

)
MANAGERS = ADMINS

INTERNAL_IPS = ("127.0.0.1",)

DBPATH = os.path.join(BASE_DIR, 'db/db.db')
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': DBPATH,                         # Or path to database file if using sqlite3.
        'USER': '',                             # Not used with sqlite3.
        'PASSWORD': '',                         # Not used with sqlite3.
        'HOST': '',                             # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                             # Set to empty string for default. Not used with sqlite3.
    }
 }


AUTH_PROFILE_MODULE = 'accounts.UserProfile'

LOGIN_URL = '/accounts/smscode/'

AUTHENTICATION_BACKENDS = (
                           'django.contrib.auth.backends.ModelBackend',
                           )

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/New_York'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = False

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = False


# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"


MEDIA_ROOT = os.path.join(BASE_DIR, 'uploads')
# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
#MEDIA_URL = 'http://127.0.0.1:8000/media/'
MEDIA_URL = '/media/'
# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'
# URL prefix for admin static files -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
# Examples: "http://foo.com/static/admin/", "/static/admin/".
ADMIN_MEDIA_PREFIX = '/static/admin/'
MAIN_STATIC_ROOT = os.path.join(BASE_DIR, 'mainstatic')
# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    MAIN_STATIC_ROOT,
    )


TEMPLATE_CONTEXT_PROCESSORS = (
    # add the current patient object in the context (patient id in URL)
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.contrib.messages.context_processors.messages",
    # "hive.apps.generic.processors.display_pre_text_segment"
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'ap^2y646_s=_^yoz64df*uefz*-jzr^pkk=ls-st&fhny+inj0'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'foodie.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(BASE_DIR, 'templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    # 'django.contrib.admindocs',
    'autofixture',
    #'south',
    'django_extensions',
    'django_ses',
    'apps.api',
    'apps.home',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'console':{
            'class':'logging.StreamHandler',
            'formatter': 'simple'
        },
        'mail_admins': {
            'level': 'ERROR', 
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'tempfile': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'verbose',
            'filename': os.path.join(tempfile.gettempdir(), 'django-debug.log'),
        },

    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
            
         'soaplib.core.server.wsgi': {
            'handlers': ['console'],
            'propagate': True,
        },
        'debug': {
            'handlers': ['tempfile', 'console'],
            'level': 'DEBUG',
        }
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.PyLibMCCache',
        'LOCATION': '127.0.0.1:11211',
    }
}

# Email Settings --------------------------------------------------------------

EMAIL_HOST_USER = 'hive@videntity.com'
#HOSTNAME_URL = 'https://hive.communityeducatyiongroup.org'
HOSTNAME_URL = 'http://127.0.0.1:8000'
EMAIL_BACKEND = 'django_ses.SESBackend'
AWS_ACCESS_KEY_ID = 'AKIAIE5XDCZ5PNK4RGOQ'
AWS_SECRET_ACCESS_KEY = '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'
DEFAULT_FROM_EMAIL='hive@videntity.com'
SERVER_EMAIL='hive@videntity.com'

# Twilio SMS Login Settings ---------------------------------------------------
TWILIO_DEFAULT_FROM = "+4107093335"
TWILIO_API_BASE = "https://api.twilio.com/2010-04-01"
TWILIO_SID = "APf8cf0431be4a49cf82166e998ad8d5f2"
TWILIO_AUTH_TOKEN = "c4c870b94031af6145c8342f13334648"
TWILIO_API_VERSION = '2010-04-01'
SMS_LOGIN_TIMEOUT_MIN = 60

# --------------------------------------------------------------------------
# HIVE Settings --------------------------------------------------------------
# --------------------------------------------------------------------------

MIN_PASSWORD_LEN=8
#Backup settings --------------------------------------------------------------
AWS_BUCKET = "cegphi"
AWS_KEY = AWS_ACCESS_KEY_ID
AWS_SECRET = AWS_SECRET_ACCESS_KEY
AWS_PUBLIC = False
AWS_FIXTURE_BACKUP_FILENAME = 'hive-fixture-backup.des3'
AWS_BIN_BACKUP_FILENAME = 'hive-bin-backup.des3'

AWS_LOCAL_FIXTURE_FILEPATH = os.path.join(BASE_DIR, 'hive-fixture-backup.des3')
AWS_LOCAL_BIN_FILEPATH = os.path.join(BASE_DIR, 'hive-bin-backup.des3')


#RESTCAT Settings
RESTCAT_SERVER = "http://127.0.0.1:8000/"
RESTCAT_USER ="hive"
RESTCAT_PASSWORD ="password"
TIMEZONE_OFFSET ="-5"


#Account Activation Settings -------------------------------------------------
ACCOUNT_ACTIVATION_DAYS = 2
RESTRICT_REG_DOMAIN_TO = None
MIN_PASSWORD_LEN = 10

# todo: make this a dictionary ?


# For running Unit Tests, copy/rename the example file found in
# ../config/settings_test.py to the same directory as settings.py
try:
    from settings_test import *
except ImportError:
    pass