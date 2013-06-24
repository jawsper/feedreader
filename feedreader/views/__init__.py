# __init__.py
# Author: Jasper Seidel
# Date: 2013-06-24

from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.views.generic.base import View
from django.core import serializers
from django.db import connection, transaction

from feedreader.models import Outline, Feed, Post, UserPost, ConfigStore

import re
import json
import urllib2, urlparse
from PIL import Image
from StringIO import StringIO

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

def outline_to_dict_with_children( request, outline, use_short_keys = False ):
	short_keys = ( 'i', 't', 'f', 'o', 'u', 'c' )
	long_keys = ( 'id', 'title', 'feed_id', 'folder_opened', 'unread_count', 'children' )
	return dict( zip(
		short_keys if use_short_keys else long_keys, [
			outline.id,
			outline.title,
			outline.feed.id if outline.feed else None,
			outline.folder_opened,
			get_unread_count( request.user, outline ),
			[ outline_to_dict_with_children( request, child, use_short_keys ) for child in Outline.objects.filter( parent = outline, user = request.user ) ]
		]
	) )

def main_navigation( request, use_short_keys = True ):
	return [ outline_to_dict_with_children( request, outline, use_short_keys ) for outline in Outline.objects.filter( parent = None, user = request.user ) ]

#def login( request ):
#	return render( request, 'feedreader/login.html' )

def camelCaseDashedDict( cfg ):
	def camelCaseDashedString( s ):
		return re.sub( r'-(\w)', lambda m: m.group(1).upper(), s )
	d = {}
	for val in cfg.values():
		d[ camelCaseDashedString( val['key'] ) ] = val['value']
	return d

@login_required
def index( request ):
	return render( request, 'feedreader/index.html', { 'config': camelCaseDashedDict( ConfigStore.objects.filter( user = request.user ) ), 'outline_list': main_navigation( request, False ) } )

@login_required
def outline( request, outline_id ):
	try:
		outline = Outline.objects.get( pk = outline_id, user = request.user.id )
	except Outline.DoesNotExist:
		raise Http404
	return render( request, 'feedreader/outline.html', { 
		'outline_list': main_navigation( request ), 
		'outline': outline,
	} )
	

class FeedFaviconView(View):
	def get( self, request, feed_id ):
		try:
			raise Exception # temporary
			self.feed = Feed.objects.get( pk = feed_id )
			if self.feed.faviconUrl:
				icon = self.load_icon( self.feed.faviconUrl )
				if icon:
					return HttpResponse( icon[0], content_type = icon[1] )
				else:
					return self.default_icon()
			
			# locate the <link> tag and find the icon in there
			icon = self.find_icon_in_page()
			if icon:
				self.save_icon( icon[2] )
				return HttpResponse( icon[0], content_type = icon[1] )
			
			# try <host>/favicon.ico
			icon = self.try_force_favicon()
			if icon:
				self.save_icon( icon[2] )
				return HttpResponse( icon[0], content_type = icon[1] )
		except:
			pass
		
		return self.default_icon()
	
	def save_icon( self, url ):
		self.feed.faviconUrl = url
		self.feed.save()
	
	def load_icon( self, url ):
		try:
			result = urllib2.urlopen( urllib2.Request( url, headers = { 'User-Agent': 'Chrome' } ) )
			data = result.read()
			content_type = result.headers.get( 'content-type' ) if 'content-type' in result.headers else 'text/html'
			img = Image.open( StringIO( data ) )
			if False and content_type == 'image/x-icon' or not img.size == (16,16):
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

