from .base import *

DEBUG = True
ALLOWED_HOSTS = []

LOAD_FAVICON = False

SECRET_KEY = "Better generate a better secret key!"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
        "NAME": "feedreader",
        "USER": "feedreader",
        "PASSWORD": "feedreader",
    }
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
