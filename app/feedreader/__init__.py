from .celery import app as celery_app

__all__ = ['celery_app']

__version__ = '1.2.10'

def get_version():
    return __version__