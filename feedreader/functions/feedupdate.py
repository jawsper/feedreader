from django.db import IntegrityError

from feedreader.models import Feed, Post, Outline, UserPost

import feedparser
import time

import datetime

import socket
socket.setdefaulttimeout( 15 )

import logging

logger = logging.getLogger(__name__)

MYSQL_DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S%z'
def compare_datetime_to_struct_time( dt, st ):
    return dt.strftime( MYSQL_DATETIME_FORMAT ) == time.strftime( MYSQL_DATETIME_FORMAT, st )

class UTC(datetime.tzinfo):
    """UTC"""
    def utcoffset(self, dt):
        return datetime.timedelta(0)
    def tzname(self, dt):
        return "UTC"
    def dst(self, dt):
        return datetime.timedelta(0)

class FeedUpdater:
    def __init__(self, stdout=None, **options):
        self.stdout = stdout
        self.imported = 0
        self.options = options

    def run(self):
        if 'range' in self.options:
            self.update_feed(range=self.options['range'])
        else:
            self.update_feed()

    def update_feed( self, feed=None, range=None):
        if feed is None and range is None:
            for feed in Feed.objects.filter(disabled=False):
                self.update_feed(feed)
        elif feed is None:
            import re
            if re.match('^\d+$', range):
                self.update_feed(feed=Feed.objects.get(pk=int(range)))
            m = re.match('^(\d+),$', range)
            if m:
                for feed in Feed.objects.filter(id__gte=int(m.groups(1)[0])):
                    self.update_feed(feed=feed)
        else:
            result = self.load_feed(feed)
            if result:
                feed.lastUpdated = datetime.datetime.utcnow().replace( tzinfo = UTC() )
                feed.lastStatus = result
                feed.save()

    def load_feed( self, feed ):
        prefix = ' ' * len(f'{feed.id:03}')
        log_message = f'{feed.id:03} {feed.xmlUrl} '
        logger.info(log_message)
        args = dict(
            etag=str(feed.lastETag),
            modified=str(feed.lastPubDate if feed.lastPubDate else feed.lastUpdated)
        )
        if feed.quirkFixNotXml:
            args['response_headers'] = {}
            args['response_headers']['Content-type'] = 'text/xml'
        data = feedparser.parse(str(feed.xmlUrl), **args)

        if 'status' in data:
            if data['status'] >= 400:
                logger.warn(f'{prefix}Failed: status error {data["status"]}')
                return 'Error: {0}'.format( data['status'] )
            elif data.status == 304:
                logger.info(f'{prefix}304 Not Changed')
                if not self.options.get('force', False):
                    return '304'

        if data['bozo']:
            logger.warn(f'{prefix}Failed: {data["bozo_exception"]}')
            return 'Error: {0}'.format( data['bozo_exception'] )
        if not data:
            logger.warn(f'{prefix}Failed: no data')
            return 'Error: no data'

        if 'etag' in data:
            if feed.lastETag != data.etag:
                feed.lastETag = data.etag
                feed.save()

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

        if feed.lastPubDate and last_updated and compare_datetime_to_struct_time( feed.lastPubDate, last_updated ):
            changed = False
        elif last_updated:
            feed.lastPubDate = time.strftime( MYSQL_DATETIME_FORMAT, last_updated )

        if not changed:
            logger.info(f'{prefix}No changes detected')
            if not self.options.get('force', False):
                return None

        logger.info(f'{prefix}scanning {len(data["entries"])} posts, please have patience...')

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
                    logger.warn('{prefix}Can\'t find a link.')
                    continue

            if 'content' in entry:
                insert_data['content'] = entry['content'][0]['value']
            if 'description' in entry:
                insert_data['description'] = entry['description']
            if 'published_parsed' in entry and entry['published_parsed']:
                try:
                    insert_data['pubDate'] = time.strftime( MYSQL_DATETIME_FORMAT, entry['published_parsed'] )
                except TypeError:
                    logger.warn('{prefix}Invalid date: {entry["published_parsed"]}')
                    continue
            elif 'updated_parsed' in entry and entry['updated_parsed']:
                insert_data['pubDate'] = time.strftime( MYSQL_DATETIME_FORMAT, entry['updated_parsed'] )

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
                    logger.warn(f'{prefix} Cannot find a good unique ID {entry} {insert_data}')
                    raise CommandError( 'See above' )
            if not 'pubDate' in insert_data:
                insert_data['pubDate'] = datetime.datetime.utcnow().replace(tzinfo=UTC())

            try:
                test = Post.objects.get( guid__exact = insert_data['guid'] )
            except Post.MultipleObjectsReturned:
                logger.info(f'{prefix}Duplicate post! {insert_data}')
            except Post.DoesNotExist:
                insert_data['feed'] = feed
                post = Post( **insert_data )
                try:
                    post.save()
                    for outline in Outline.objects.filter( feed = feed ):
                        outline.unread_count += 1
                        outline.save()
                        UserPost( user = outline.user, post = post ).save() # make userposts for all users who have this feed
                    imported += 1
                except IntegrityError:
                    logger.warn(f'{prefix}IntegrityError: {entry}')
                    raise CommandError( 'Invalid post' )

        logger.info(f'{prefix}Inserted {imported} new posts')
        self.imported += imported
        return 'OK'
