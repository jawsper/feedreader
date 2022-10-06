from celery import shared_task
import asyncio

from feedreader.functions.feedupdate import FeedsUpdater
from feedreader.models import Feed
from feedreader.functions import find_favicon

import logging

logger = logging.getLogger(__name__)


@shared_task(ignore_result=True)
def update():
    logger.info("Starting feedupdate")
    updater = FeedsUpdater()
    asyncio.run(updater.run())
    logger.info("Feedupdate completed, {} feeds updated".format(updater.imported))


@shared_task(ignore_result=True)
def add_feed(user, url):
    logger.info("add_feed: %s, %s", user, url)


@shared_task(ignore_result=True)
def update_feed(feed_id):
    try:
        feed = Feed.objects.get(pk=feed_id)
    except Feed.DoesNotExist:
        return
    updater = FeedsUpdater()
    asyncio.run(updater.update_feed(feed))


@shared_task(ignore_result=True)
def download_feed_favicon(feed_id):
    logger.info(f"Finding favicon for feed {feed_id}")
    try:
        feed = Feed.objects.get(pk=feed_id)
    except Feed.DoesNotExist:
        logger.warning(f"Feed {feed_id} doesn't exist")
        return
    if not feed.favicon_url:
        logger.info("No favicon URL set, trying to find one")
        feed.favicon_url = find_favicon(feed)
        feed.save(update_fields=["favicon_url"])
        logger.info(f"URL is now: {feed.favicon_url}")
    logger.info("Downloading favicon")
    result = feed.download_favicon()
    logger.info(f"Download success: {result}")
