from .base import *

import os
import raven

DEBUG = False

ALLOWED_HOSTS = [os.environ.get('DJANGO_ALLOWED_HOST')]

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')

ADMINS = ((
    os.environ.get('ADMIN_EMAIL_NAME', ''),
    os.environ.get('ADMIN_EMAIL_ADDRESS', '')
),)

DATABASES = {
   'default': {
       'ENGINE': 'django.db.backends.postgresql_psycopg2',
       'NAME': os.environ.get('DB_NAME', ''),
       'USER': os.environ.get('DB_USER', '')
   }
}

STATIC_ROOT = os.path.join(BASE_DIR, os.environ.get('STATIC_ROOT', "static/"))
STATIC_URL = os.environ.get('STATIC_URL', STATIC_URL)

MEDIA_ROOT = os.path.join(BASE_DIR, os.environ.get('MEDIA_ROOT', "media/"))
MEDIA_URL = os.environ.get('MEDIA_URL', "/media/")

RAVEN_CONFIG = {
    'dsn': os.environ.get('SENTRY_DSN'),
    'release': raven.fetch_git_sha(PROJECT_PATH),
}
