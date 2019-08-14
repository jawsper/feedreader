from .base import *

from feedreader import __version__

import os
import pkg_resources
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

DEBUG = False

ALLOWED_HOSTS = [os.environ.get('DJANGO_ALLOWED_HOST')]

SECRET_KEY = open('/var/run/secrets/secret_key', 'rt').read()

ADMINS = ((
    os.environ.get('ADMIN_EMAIL_NAME', ''),
    os.environ.get('ADMIN_EMAIL_ADDRESS', '')
),)

DATABASES = {
  'default': {
    'ENGINE': os.getenv('SQL_ENGINE', 'django.db.backends.sqlite3'),
    'NAME': os.getenv('SQL_DATABASE', os.path.join(BASE_DIR, 'db.sqlite3')),
    'USER': os.getenv('SQL_USER', 'user'),
    'PASSWORD': os.getenv('SQL_PASSWORD', 'password'),
    'HOST': os.getenv('SQL_HOST', 'localhost'),
    'PORT': os.getenv('SQL_PORT', '5432'),
  }
}

STATIC_ROOT = os.path.join(BASE_DIR, os.environ.get('STATIC_ROOT', "static/"))
STATIC_URL = os.environ.get('STATIC_URL', STATIC_URL)

MEDIA_ROOT = os.path.join(BASE_DIR, os.environ.get('MEDIA_ROOT', "media/"))
MEDIA_URL = os.environ.get('MEDIA_URL', MEDIA_URL)

sentry_sdk.init(
  os.environ.get('SENTRY_DSN'),
  integrations=[DjangoIntegration()],
  release=f'feedreader@{__version__}'
)

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_PATH = '/feedreader/'
CSRF_COOKIE_PATH = '/feedreader/'
