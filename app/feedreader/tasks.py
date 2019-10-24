from celery import shared_task
import asyncio

from feedreader.functions.feedupdate import FeedUpdater
from feedreader.models import Outline, Feed
from feedreader.functions import get_unread_count, find_favicon

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

@shared_task(ignore_result=True)
def download_feed_favicon(feed_id):
    logger.info(f'Finding favicon for feed {feed_id}')
    try:
        feed = Feed.objects.get(pk=feed_id)
    except Feed.DoesNotExist:
        logger.warning(f'Feed {feed_id} doesn\'t exist')
        return
    if not feed.faviconUrl:
        logger.info('No favicon URL set, trying to find one')
        feed.faviconUrl = find_favicon(feed)
        feed.save(update_fields=['faviconUrl'])
        logger.info(f'URL is now: {feed.faviconUrl}')
    logger.info('Downloading favicon')
    result = feed.download_favicon()
    logger.info(f'Download success: {result}')

