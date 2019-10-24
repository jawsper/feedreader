#
# Author: Jasper Seidel
# Date: 2013-06-28

from django.core.management.base import BaseCommand

from feedreader.functions import FaviconFinder
from feedreader.models import Feed

import socket
socket.setdefaulttimeout( 15 )

class Command( BaseCommand ):
    def add_arguments(self, parser):
        parser.add_argument('feed_id', nargs="?")

    def handle( self, *args, feed_id=None, **options ):
        self.stdout.write( '[Favicon finder]' )
        
        if feed_id is not None:
            feeds = Feed.objects.filter(pk=feed_id)
        else:
            feeds = Feed.objects.all()
        
        for feed in feeds:
            if feed_id is not None or feed.faviconUrl == None or feed.faviconUrl == '':
                self.stdout.write( '{0:03} {1} '.format( feed.id, feed.xmlUrl ) )
                self.stdout.write( ' * htmlUrl: {}'.format( feed.htmlUrl ) )
                print(FaviconFinder( feed, self.stdout ).find())
                FaviconFinder( feed, self.stdout ).find_and_save()
