from typing import List
from .base import *

DEBUG = True
ALLOWED_HOSTS: List[str] = []

LOAD_FAVICON = False

SECRET_KEY = "Better generate a better secret key!"

DATABASES = {
    "default": {
        "ENGINE": os.getenv("SQL_ENGINE", "django.db.backends.sqlite3"),
        "NAME": os.getenv("SQL_DATABASE", BASE_DIR / "develop.sqlite3"),
        "USER": "feedreader",
        "PASSWORD": "feedreader",
    }
}

INSTALLED_APPS += ["debug_toolbar"]
MIDDLEWARE = ["debug_toolbar.middleware.DebugToolbarMiddleware"] + MIDDLEWARE

INTERNAL_IPS = [
    "127.0.0.1",
    "::1",
]

DEBUG_TOOLBAR_CONFIG = {
    "RESULTS_CACHE_SIZE": 100,
}

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "django.server": {
            "()": "django.utils.log.ServerFormatter",
            "format": "[{server_time}] {message}",
            "style": "{",
        },
        "console": {
            "format": "[{asctime}] - {name} - {levelname} - {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "console",
        },
        "django.server": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "django.server",
        },
    },
    "loggers": {
        # 'django': {
        #     'handlers': ['console'],
        #     'level': 'INFO',
        # },
        "django.server": {
            "level": "INFO",
            "handlers": ["django.server"],
            "propagate": False,
        },
        # 'django.db.backends': {
        #     'level': 'DEBUG',
        #     'handlers': ['console'],
        # },
        "feedreader": {
            "level": "DEBUG",
            "handlers": ["console"],
        },
    },
}
