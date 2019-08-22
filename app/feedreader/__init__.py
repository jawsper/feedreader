from .celery import app as celery_app

__all__ = ['celery_app']

__version__ = '1.4.1'

def get_version():
    return __version__
