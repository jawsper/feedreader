# functions/__init__.py
# Author: Jasper Seidel
# Date: 2013-06-29

from django.http import HttpResponse
from django.db import connection
from django.utils.timezone import utc
from feedreader.models import Outline, UserToken, Feed

# subfunctions
from feedreader.functions.feeds import add_feed

import re
import json
import datetime


class HttpJsonResponse( HttpResponse ):
	def __init__( self, data = None, **kwargs ):
		HttpResponse.__init__( self, json.dumps( data if data else kwargs ), content_type = 'application/json' )

def get_unread_count( user, outline ):
	cursor = connection.cursor()
	if outline.feed:
		cursor.execute( 'select count(Post.id) ' + 
		'from feedreader_post Post left outer join feedreader_userpost UserPost on ( Post.id = UserPost.post_id and UserPost.user_id = %s ) ' + 
		'where Post.feed_id = %s and ( UserPost.read is null or UserPost.read = 0 )', [ user.id, outline.feed.id ]  )
		unread_count = cursor.fetchone()
	else:
		cursor.execute( 'select count(Post.id) ' + 
		'from feedreader_post Post left outer join feedreader_userpost UserPost on ( Post.id = UserPost.post_id and UserPost.user_id = %s ) ' + 
		'where Post.feed_id in ( select feed_id from feedreader_outline where parent_id = %s ) and ( UserPost.read is null or UserPost.read = 0 )', [ user.id, outline.id ] )
		unread_count = cursor.fetchone()
	cursor.close()
	return unread_count[0] if unread_count else None

def get_total_unread_count( user ):
	cursor = connection.cursor()
	cursor.execute( 'select count(Post.id) ' +
		'from feedreader_post Post left outer join feedreader_userpost UserPost on ( Post.id = UserPost.post_id and UserPost.user_id = %s )' +
		'where Post.feed_id in ( select feed_id from feedreader_outline Outline where feed_id is not null and user_id = %s ) ' +
		' and ( UserPost.read is null or UserPost.read = 0 )', [ user.id, user.id ] )
	count = cursor.fetchone()
	cursor.close()
	return count[0] if count else None

def outline_to_dict_with_children( request, outline, use_short_keys = False ):
	short_keys = ( 'i', 't', 'f', 'fi', 'o', 'u', 'c' )
	long_keys = ( 'id', 'title', 'feed_id', 'faviconUrl', 'folder_opened', 'unread_count', 'children' )
	return dict( zip(
		short_keys if use_short_keys else long_keys, [
			outline.id,
			outline.title,
			outline.feed.id if outline.feed else None,
			outline.feed.faviconUrl if outline.feed else None,
			outline.folder_opened,
			get_unread_count( request.user, outline ),
			[ outline_to_dict_with_children( request, child, use_short_keys ) for child in Outline.objects.select_related().filter( parent = outline, user = request.user ) ]
		]
	) )

def main_navigation( request, use_short_keys = True ):
	if 'use_long_keys' in request.POST:
		use_short_keys = False
	return [ outline_to_dict_with_children( request, outline, use_short_keys ) for outline in Outline.objects.select_related().filter( parent = None, user = request.user ) ]

def verify_token( username, token ):
	if not username or not token:
		return False
	try:
		token = UserToken.objects.get( user__username = username, token = token )
		if token.expire < datetime.datetime.utcnow().replace( tzinfo = utc ): # invalid token
			token.delete()
			return False
		return token
	except UserToken.DoesNotExist:
		pass
	return False


import re
import urllib2, urlparse
from PIL import Image
from StringIO import StringIO

class FaviconFinder:
	def __init__( self, feed, stdout ):
		self.feed = feed
		self.stdout = stdout
		
	def find( self ):
		# locate the <link> tag and find the icon in there
		self.stdout.write( ' * Trying to find icon in html page' )
		icon = self.find_icon_in_page()
		if icon:
			self.save_icon( icon[2] )
			return
		
		# try <host>/favicon.ico
		self.stdout.write( ' * Trying <host>/favicon.ico' )
		icon = self.try_force_favicon()
		if icon:
			self.save_icon( icon[2] )
			return
		
		self.stdout.write( ' * No icon found...' )
	
	def save_icon( self, url ):
		self.stdout.write( ' * Found icon at {}'.format( url ) )
		self.feed.faviconUrl = url
		self.feed.save()
	
	def load_icon( self, url ):
		try:
			result = urllib2.urlopen( urllib2.Request( url, headers = { 'User-Agent': 'Chrome' } ) )
			data = result.read()
			content_type = result.headers.get( 'content-type' ) if 'content-type' in result.headers else 'text/html'
			img = Image.open( StringIO( data ) )
			if False and ( content_type == 'image/x-icon' or not img.size == (16,16) ):
				if not img.size == (16,16):
					print( 'resizing' )
					img = img.resize( ( 16, 16 ) )
				raw = StringIO()
				img.save( raw, 'PNG' )
				data = raw.getvalue()
				content_type = 'image/png'
			return ( data, content_type, url )
		except Exception as e:
			print( "Exception in load_icon: {0}".format( e ) )
			return False
	
	def find_icon_in_page( self ):
		# load associated html page
		try:
			data = urllib2.urlopen( urllib2.Request( self.feed.htmlUrl, headers = { 'User-Agent': 'Chrome' } ) ).read()
			matches = re.findall( '<link ([^>]+)>', data )
			for match in matches:
				if re.search( 'rel="(shortcut )?icon"', match ):
					m = re.search( 'href="([^"]+)"', match )
					if not m:
						continue
				
					favicon_url = m.groups(1)[0]
				
					p_favicon_url = urlparse.urlparse( favicon_url )
				
					# relative url, add hostname of site
					if not p_favicon_url.hostname:
						p_url = urlparse.urlparse( self.feed.htmlUrl )
						favicon_url = urlparse.urlunparse( p_url[0:2] + p_favicon_url[2:] )
				
					return self.load_icon( favicon_url )
		except:
			pass
		return False
	
	def try_force_favicon( self ):
		p_url = urlparse.urlparse( self.feed.htmlUrl )
		return self.load_icon( '{0}://{1}/favicon.ico'.format( p_url[0], p_url[1] ) )
	
	def default_icon( self ):
		return HttpResponse( open( settings.STATIC_ROOT + 'images/icons/silk/feed.png', 'r' ).read(), content_type = 'image/png' )

