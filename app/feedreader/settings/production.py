from .base import *

from feedreader import __version__

import os
from pathlib import Path
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.celery import CeleryIntegration
from sentry_sdk.integrations.aiohttp import AioHttpIntegration
from sentry_sdk.integrations.redis import RedisIntegration

DEBUG = False

ALLOWED_HOSTS = [os.getenv("DJANGO_ALLOWED_HOST")]

if secret_key := os.getenv("DJANGO_SECRET_KEY"):
    SECRET_KEY = secret_key
else:
    SECRET_KEY = Path(
        os.getenv("DJANGO_SECRET_KEY_PATH", "/var/run/secrets/secret_key")
    ).read_text()

ADMINS = ((os.getenv("ADMIN_EMAIL_NAME", ""), os.getenv("ADMIN_EMAIL_ADDRESS", "")),)

DATABASES = {
    "default": {
        "ENGINE": os.getenv("SQL_ENGINE", "django.db.backends.sqlite3"),
        "NAME": os.getenv("SQL_DATABASE", str(BASE_DIR / "db.sqlite3")),
        "USER": os.getenv("SQL_USER", "user"),
        "PASSWORD": os.getenv("SQL_PASSWORD", "password"),
        "HOST": os.getenv("SQL_HOST", "localhost"),
        "PORT": os.getenv("SQL_PORT", "5432"),
    }
}

STATIC_ROOT = os.getenv("STATIC_ROOT", str(BASE_DIR / "static/"))
STATIC_URL = os.getenv("STATIC_URL", STATIC_URL)

MEDIA_ROOT = os.getenv("MEDIA_ROOT", str(BASE_DIR / "media/"))
MEDIA_URL = os.getenv("MEDIA_URL", MEDIA_URL)

sentry_sdk.init(
    os.getenv("SENTRY_DSN"),
    integrations=[
        DjangoIntegration(),
        CeleryIntegration(),
        AioHttpIntegration(),
        RedisIntegration(),
    ],
    release=f"feedreader@{__version__}",
)

SESSION_COOKIE_SECURE = os.getenv("SESSION_COOKIE_SECURE", "True") == "True"
SESSION_COOKIE_PATH = os.getenv("SESSION_COOKIE_PATH", "/")
SESSION_COOKIE_SAMESITE = os.getenv("SESSION_COOKIE_SAMESITE", "Strict")
CSRF_COOKIE_SECURE = os.getenv("CSRF_COOKIE_SECURE", "True") == "True"
CSRF_COOKIE_PATH = os.getenv("CSRF_COOKIE_PATH", "/")
CSRF_COOKIE_SAMESITE = os.getenv("CSRF_COOKIE_SAMESITE", "Strict")

CSRF_TRUSTED_ORIGINS = os.getenv("CSRF_TRUSTED_ORIGINS", "").split(",")

CORS_ALLOWED_ORIGINS = os.getenv("CORS_ALLOWED_ORIGINS", "").split(",")
CORS_ALLOW_CREDENTIALS = True
