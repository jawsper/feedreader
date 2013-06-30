# __init__.py
# Author: Jasper Seidel
# Date: 2013-06-24

from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.views.generic.base import View

from feedreader.models import Outline, Feed, Post, UserPost, ConfigStore

from feedreader.functions import main_navigation

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

import re
import urllib2, urlparse
from PIL import Image
from StringIO import StringIO

@login_required
def index( request ):
	return render( request, 'feedreader/index.html', {
		'config': ConfigStore.getUserConfig( user = request.user ),
		'outline_list': main_navigation( request, False )
	} )

class FeedFaviconView( View ):
	@method_decorator( cache_page( 60 * 15 ) )
	def dispatch( self, *args, **kwargs ):
		return View.dispatch( self, *args, **kwargs )

	def get( self, request, feed_id ):
		try:
			feed = Feed.objects.get( pk = feed_id )
			if feed.faviconUrl:
				icon = self.load_icon( feed.faviconUrl )
				if icon:
					return HttpResponse( icon[0], content_type = icon[1] )
		except Feed.DoesNotExist:
			pass
		
		return self.default_icon()
	
	
	def load_icon( self, url ):
		try:
			result = urllib2.urlopen( urllib2.Request( url, headers = { 'User-Agent': 'Chrome' } ) )
			data = result.read()
			content_type = result.headers.get( 'content-type' ) if 'content-type' in result.headers else 'text/html'
			img = Image.open( StringIO( data ) )
			#if content_type == 'image/x-icon' or not img.size == (16,16):
			#	if not img.size == (16,16):
			#		print( 'resizing' )
			#		img = img.resize( ( 16, 16 ) )
			#	raw = StringIO()
			#	img.save( raw, 'PNG' )
			#	data = raw.getvalue()
			#	content_type = 'image/png'
			return ( data, content_type, url )
		except Exception as e:
			print( "Exception in load_icon: {0}".format( e ) )
			return False
	
	def default_icon( self ):
		return HttpResponse( open( settings.STATIC_ROOT + 'images/icons/silk/feed.png', 'r' ).read(), content_type = 'image/png' )

