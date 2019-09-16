from django.db import IntegrityError
from django.utils import timezone

from feedreader import __version__
from feedreader.models import Feed, Post, Outline, UserPost

import feedparser
import time
import asyncio
import aiohttp
from time import mktime
from wsgiref.handlers import format_date_time
import re
from urllib.parse import urlparse

import datetime

import socket
socket.setdefaulttimeout( 15 )

import logging

logger = logging.getLogger(__name__)


def struct_time_to_aware_datetime(time):
    return datetime.datetime(*time[:6]).replace(tzinfo=timezone.utc)


class FeedUpdater:
    def __init__(self, stdout=None, **options):
        self.stdout = stdout
        self.imported = 0
        self.options = options
        self.session = None

    def get_session(self):
        if not self.session:
            self.session = aiohttp.ClientSession(headers={
                'A-IM': 'feed', # RFC 3229 support
                'User-Agent': f'feedreader/{__version__}+https://github.com/jawsper/feedreader',
                "Accept": "application/atom+xml,application/rdf+xml,application/rss+xml,application/x-netcdf,application/xml;q=0.9,text/xml;q=0.2,*/*;q=0.1",
            })
        return self.session

    async def run(self):
        range_ = self.options.get('range', None)
        qs = None
        if range_:
            if re.match(r'^\d+$', range_):
                qs = Feed.objects.filter(pk=int(range_))
            else:
                m = re.match(r'^(\d+),$', range_)
                if m:
                    qs = Feed.objects.filter(id__gte=int(m.group(1)))
        else:
            qs = Feed.objects.filter(disabled=False)
        if qs:
            async with self.get_session() as self.session:
                await asyncio.gather(*(self._update_feed(feed) for feed in qs))

    async def update_feed(self, feed):
        async with self.get_session() as self.session:
            await self._update_feed(feed=feed)

    async def _update_feed(self, feed):
        result = await self.load_feed(feed=feed)
        if result:
            feed.lastUpdated = timezone.now()
            feed.lastStatus = result
            feed.save()

    async def download_feed(self, feed):
        try:
            headers = {}
            if not self.options.get('force', False):
                if feed.lastETag:
                    headers['If-None-Match'] = feed.lastETag
                modified = feed.lastPubDate if feed.lastPubDate else feed.lastUpdated
                if modified:
                    modified = mktime(modified.timetuple())
                    headers['If-Modified-Since'] = format_date_time(modified)
            hostname = urlparse(feed.xmlUrl).hostname
            if hostname.endswith('.tumblr.com'):
                headers['User-Agent'] = 'Mozilla/5.0 (compatible; Baiduspider; +http://www.baidu.com/search/spider.html)'
            async with self.session.get(feed.xmlUrl, headers=headers) as response:
                return (await response.text()), response
        except aiohttp.ClientError as e:
            print(f'{feed.id:03} | error | {e}')
            return None, None

    async def load_feed(self, feed: Feed):
        prefix = f'[{feed.id:03}] '
        logger.info(f'{prefix}{feed.xmlUrl}')
        raw_data, response = await self.download_feed(feed=feed)
        if not response:
            return None

        if response.status >= 400:
            logger.warn(f'{prefix}Failed: status error {response.status}')
            return f'Error: {response.status}'
        elif response.status == 304:
            logger.info(f'{prefix}304 Not Changed')
            if not self.options.get('force', False):
                return '304'

        data = feedparser.parse(raw_data)

        if data['bozo']:
            logger.warn('{}Failed: {}'.format(prefix, data["bozo_exception"]))
        if not data:
            logger.warn('{}Failed: no data'.format(prefix))
            return 'Error: no data'

        if response.headers.get('etag'):
            if feed.lastETag != response.headers.get('etag'):
                feed.lastETag = response.headers.get('etag')
                feed.save(update_fields=['lastETag'])

        changed = True
        last_updated = None

        if 'feed' in data and 'updated_parsed' in data['feed']:
            last_updated = data['feed']['updated_parsed']
        elif 'feed' in data and 'published_parsed' in data['feed']:
            last_updated = data['feed']['published_parsed']
        elif 'updated_parsed' in data:
            last_updated = data['updated_parsed']
        elif 'published_parsed' in data:
            last_updated = data['published_parsed']

        if last_updated:
            last_updated = struct_time_to_aware_datetime(last_updated)

        if feed.quirk_fix_invalid_publication_date:
            pass
        elif feed.lastPubDate and last_updated and feed.lastPubDate == last_updated:
            changed = False
        elif last_updated:
            feed.lastPubDate = last_updated
            feed.save(update_fields=["lastPubDate"])

        if not changed:
            logger.info('{}No changes detected'.format(prefix))
            if not self.options.get('force', False):
                return None

        logger.info('{}scanning {} posts, please have patience...'.format(prefix, len(data["entries"])))

        imported = 0

        for entry in data['entries']:
            insert_data = {}
            if 'title' in entry:
                insert_data['title'] = entry['title']

            if 'author_detail' in entry and 'name' in entry['author_detail']:
                insert_data['author'] = entry['author_detail']['name']

            if 'links' in entry:
                if len( entry['links'] ) == 0:
                    pass
                elif len( entry['links'] ) == 1:
                    insert_data['link'] = entry['links'][0]['href']
                else:
                    for link in entry['links']:
                        if link['rel'] == 'self':
                            insert_data['link'] = link['href']
                            break

            if not 'link' in insert_data:
                if 'link' in entry:
                    insert_data['link'] = entry['link']
                else:
                    logger.warn('{}Can\'t find a link.'.format(prefix))
                    continue

            if 'content' in entry:
                insert_data['content'] = entry['content'][0]['value']
            if 'description' in entry:
                insert_data['description'] = entry['description']
            if 'published_parsed' in entry and entry['published_parsed']:
                try:
                    insert_data['pubDate'] = struct_time_to_aware_datetime(entry['published_parsed'])
                except TypeError:
                    logger.warn('{}Invalid date: {}'.format(prefix, entry["published_parsed"]))
                    continue
            elif 'updated_parsed' in entry and entry['updated_parsed']:
                insert_data['pubDate'] = struct_time_to_aware_datetime(entry['updated_parsed'])

            if 'id' in entry:
                insert_data['guid'] = entry['id']
            if not 'guid' in insert_data:
                if 'pubDate' in insert_data:
                    insert_data['guid'] = insert_data['pubDate']
                elif 'link' in insert_data:
                    insert_data['guid'] = insert_data['link']
                elif 'description' in insert_data:
                    insert_data['guid'] = insert_data['description']
                else:
                    logger.warn('{} Cannot find a good unique ID {} {}'.format(prefix, entry, insert_data))
                    raise CommandError( 'See above' )
            if not 'pubDate' in insert_data:
                insert_data['pubDate'] = timezone.now()

            try:
                test = Post.objects.get( guid__exact = insert_data['guid'] )
            except Post.MultipleObjectsReturned:
                logger.info('{}Duplicate post! {}'.format(prefix, insert_data))
            except Post.DoesNotExist:
                insert_data['feed'] = feed
                post = Post( **insert_data )
                try:
                    post.save()
                    for outline in Outline.objects.filter( feed = feed ):
                        outline.unread_count += 1
                        outline.save(update_fields=["unread_count"])
                        UserPost( user = outline.user, post = post ).save() # make userposts for all users who have this feed
                    imported += 1
                except IntegrityError:
                    logger.warn('{}IntegrityError: {}'.format(prefix, entry))
                    raise CommandError( 'Invalid post' )

        if feed.quirk_fix_invalid_publication_date:
            try:
                feed.lastPubDate = feed.post_set.order_by('-pubDate').values_list('pubDate')[0][0]
                feed.save(update_fields=["lastPubDate"])
            except IndexError:
                pass

        logger.info('{}Inserted {} new posts'.format(prefix, imported))
        self.imported += imported
        return 'OK'
