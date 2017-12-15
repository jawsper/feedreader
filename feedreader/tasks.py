from celery import shared_task

from feedreader.functions.feedupdate import FeedUpdater
from feedreader.models import Outline
from feedreader.functions import get_unread_count

@shared_task(ignore_result=True)
def update():
    updater = FeedUpdater()
    updater.run()

    for outline in Outline.objects.all():
        outline.unread_count = get_unread_count(outline.user, outline)
        outline.save()
