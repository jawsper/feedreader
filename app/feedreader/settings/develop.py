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

DEBUG_TOOLBAR_PANELS = [
    "ddt_request_history.panels.request_history.RequestHistoryPanel",  # Here it is
    "debug_toolbar.panels.versions.VersionsPanel",
    "debug_toolbar.panels.timer.TimerPanel",
    "debug_toolbar.panels.settings.SettingsPanel",
    "debug_toolbar.panels.headers.HeadersPanel",
    "debug_toolbar.panels.request.RequestPanel",
    "debug_toolbar.panels.sql.SQLPanel",
    "debug_toolbar.panels.staticfiles.StaticFilesPanel",
    "debug_toolbar.panels.templates.TemplatesPanel",
    "debug_toolbar.panels.cache.CachePanel",
    "debug_toolbar.panels.signals.SignalsPanel",
    "debug_toolbar.panels.logging.LoggingPanel",
    "debug_toolbar.panels.redirects.RedirectsPanel",
    "debug_toolbar.panels.profiling.ProfilingPanel",
]

DEBUG_TOOLBAR_CONFIG = {
    "RESULTS_CACHE_SIZE": 100,
    "RESULTS_STORE_SIZE": 100,
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
