#
# Author: Jasper Seidel
# Date: 2013-06-28

from django.core.management.base import BaseCommand

from feedreader.functions import FaviconFinder
from feedreader.models import Feed

import socket
socket.setdefaulttimeout( 15 )

class Command( BaseCommand ):
	def handle( self, *args, **options ):
		self.stdout.write( '[Favicon loader]' )
		
		if( len( args ) > 0 ):
			feeds = Feed.objects.filter( pk__in = args )
		else:
			feeds = Feed.objects.all()
		
		for feed in feeds:
			if feed.faviconUrl == None or feed.faviconUrl == '':
				self.stdout.write( '{0:03} {1} '.format( feed.id, feed.xmlUrl ) )
				self.stdout.write( ' * htmlUrl: {}'.format( feed.htmlUrl ) )
				FaviconFinder( feed, self.stdout ).find()