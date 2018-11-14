import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'feedreader.settings.develop')

from django.conf import settings

app = Celery('feedreader')
app.config_from_object(settings.CELERY)
app.autodiscover_tasks()

@app.task
def test(arg):
    print(arg)

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
