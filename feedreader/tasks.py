from celery import shared_task

from feedreader.functions.feedupdate import FeedUpdater
from feedreader.models import Outline
from feedreader.functions import get_unread_count

import logging
logger = logging.getLogger(__name__)

@shared_task(ignore_result=True)
def update():
    logger.info('Starting feedupdate')
    updater = FeedUpdater()
    updater.run()
    logger.info('Feedupdate completed, {} feeds updated'.format(updater.imported))

    logger.info('Starting update unread count')
    for outline in Outline.objects.all():
        outline.unread_count = get_unread_count(outline.user, outline)
        outline.save()
    logger.info('Finished update unread count')
