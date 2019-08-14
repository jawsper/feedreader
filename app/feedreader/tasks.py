from celery import shared_task
import asyncio

from feedreader.functions.feedupdate import FeedUpdater
from feedreader.models import Outline, Feed
from feedreader.functions import get_unread_count

import logging
logger = logging.getLogger(__name__)

@shared_task(ignore_result=True)
def update():
    logger.info('Starting feedupdate')
    updater = FeedUpdater()
    asyncio.run(updater.run())
    logger.info('Feedupdate completed, {} feeds updated'.format(updater.imported))

    logger.info('Starting update unread count')
    for outline in Outline.objects.all():
        outline.unread_count = get_unread_count(outline.user, outline)
        outline.save()
    logger.info('Finished update unread count')

@shared_task(ignore_result=True)
def add_feed(user, url):
    logger.info('add_feed: %s, %s', user, url)

@shared_task(ignore_result=True)
def update_feed(feed_id):
    try:
        feed = Feed.objects.get(pk=feed_id)
    except Feed.DoesNotExist:
        return
    updater = FeedUpdater()
    asyncio.run(updater.update_feed(feed))
