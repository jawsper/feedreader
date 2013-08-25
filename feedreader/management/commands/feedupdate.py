from __future__ import print_function
from django.core.management.base import BaseCommand, CommandError
from django.db import IntegrityError
from optparse import make_option

from feedreader.models import Feed, Post, Outline, UserPost

import feedparser
import time

import datetime

import socket
socket.setdefaulttimeout( 15 )

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

class Command(BaseCommand):
	option_list = BaseCommand.option_list + (
		make_option( '--debug', action = 'store_true', dest = 'debug', default = False, help = 'Debug' ),
	)

	def handle( self, *args, **options ):
		self.stdout.write( '[Feed updater]' )
		self.imported = 0
		self.debug = options['debug']
		
		if len( args ) == 1:
			import re
			if re.match( '^\d+$', args[0] ):
				self.update_feed( Feed.objects.get( pk = int( args[0] ) ) )
				return
			m = re.match( '^(\d+),$', args[0] )
			if m:
				for feed in Feed.objects.filter( id__gte = int( m.groups(1)[0] ) ):
					self.update_feed( feed )
				return
		for feed in Feed.objects.filter( disabled = False ):
			self.update_feed( feed )
		self.stdout.write( 'Done! Total posts imported: {0}'.format( self.imported ) )

	def update_feed( self, feed ):
		result = self.load_feed( feed )
		if result:
			feed.lastUpdated = datetime.datetime.utcnow().replace( tzinfo = UTC() )
			feed.lastStatus = result
			feed.save()
	
	def load_feed( self, feed ):
		self.stdout.write( '{0:03} {1} '.format( feed.id, feed.xmlUrl ), ending='' )
		self.stdout.flush()
		data = feedparser.parse( str( feed.xmlUrl ) )
		
		if 'status' in data and data['status'] >= 400:
			self.stdout.write( 'Failed: status error {0}'.format( data['status'] ) )
			return 'Error: {0}'.format( data['status'] )
		if 'bozo_exception' in data:
			self.stdout.write( 'Failed: {0}'.format( data['bozo_exception'] ) )
			return 'Error: {0}'.format( data['bozo_exception'] )
		if not data:
			self.stdout.write( 'Failed: no data' )
			return 'Error: no data'
		
		self.stdout.write( 'ok!' )
		
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
			self.stdout.write( ' - No changes detected' )
			return None
		
		self.stdout.write( ' - scanning {0} posts, please have patience...'.format( len( data['entries'] ) ) )
		
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
					self.stdout.write( 'Can\'t determine a link' )
					continue
			
			if 'content' in entry:
				insert_data['content'] = entry['content'][0]['value']
			if 'description' in entry:
				insert_data['description'] = entry['description']
			if 'published_parsed' in entry and entry['published_parsed']:
				try:
					insert_data['pubDate'] = time.strftime( MYSQL_DATETIME_FORMAT, entry['published_parsed'] )
				except TypeError:
					self.stdout.write( 'Invalid date: {0}'.format( entry['published_parsed'] ) )
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
					self.stdout.write( 'Cannot find a good unique ID' )
					self.stdout.write( str( entry ) )
					self.stdout.write( str( insert_data ) )
					raise CommandError( 'See above' )
			if not 'pubDate' in insert_data:
				insert_data['pubDate'] = datetime.datetime.utcnow().replace(tzinfo=UTC())

			try:
				test = Post.objects.get( guid__exact = insert_data['guid'] )
			except Post.DoesNotExist:
				insert_data['feed'] = feed
				post = Post( **insert_data )
				try:
					post.save()
					for outline in Outline.objects.filter( feed = feed ):
					    UserPost( user = outline.user, post = post ).save() # make userposts for all users who have this feed
					imported += 1
				except IntegrityError:
					self.stdout.write( str( entry ) )
					raise CommandError( 'Invalid post' )
		
		self.stdout.write( ' - Inserted {0} new posts'.format( imported ) )
		self.imported += imported
		return 'OK'
