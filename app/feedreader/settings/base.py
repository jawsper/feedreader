"""
Django settings for feedreader project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/


# Application definition

DJANGO_CORE_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)

FEEDREADER_APPS = (
    'feedreader',
    'feedreader_gui',
    'feedreader_api',
)

THIRD_PARTY_APPS = (
    'mptt',
    'django_extensions',
    'django_celery_beat',
)

INSTALLED_APPS = DJANGO_CORE_APPS + FEEDREADER_APPS + THIRD_PARTY_APPS

MIDDLEWARE = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'feedreader.urls'

WSGI_APPLICATION = 'feedreader.wsgi.application'

LOGIN_REDIRECT_URL = 'index'
LOGOUT_REDIRECT_URL = 'index'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

LOGIN_URL = 'login'
LOGOUT_URL = 'logout'

# AUTHENTICATION_BACKENDS = (
#         'django.contrib.auth.backends.ModelBackend',
#         'feedreader.backend.TokenBackend',
# )

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'debug': False,
            # ... some options here ...
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.static',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

REDIS_HOST = os.environ.get('REDIS_HOST', 'localhost')
REDIS_PORT = int(os.environ.get('REDIS_PORT', 6379))

CELERY_BROKER_URL = f'redis://{REDIS_HOST}:{REDIS_PORT}/0'
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'
