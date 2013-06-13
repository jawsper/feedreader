# Create your views here.

from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.conf import settings
from django.views.generic.base import View
from django.utils import simplejson

from feedreader.models import Outline, Feed, Post, UserPost

import urllib2, urlparse
from PIL import Image
from StringIO import StringIO

def outline_to_dict_with_children( outline ):
	return {
		'id': outline.id,
		'title': outline.title,
		'feed_id': outline.feed.id if outline.feed else None,
		'children': map( lambda x: outline_to_dict_with_children( x ), Outline.objects.filter( parent_id = outline.id ) ),
	}
	
def main_navigation( request ):
	return map( lambda x: outline_to_dict_with_children( x ), Outline.objects.filter( parent_id = None, user = request.user.id ) )

#def login( request ):
#	return render( request, 'feedreader/login.html' )

@login_required
def index( request ):
	return render( request, 'feedreader/index.html', { 'outline_list': main_navigation( request ) } )

@login_required
def outline( request, outline_id ):
	try:
		outline = Outline.objects.get( pk = outline_id, user = request.user.id )
	except Outline.DoesNotExist:
		raise Http404
	if outline.feed:
		posts = Post.objects.filter( feed = outline.feed ).order_by( '-pubDate' )
	else:
		feeds = Outline.objects.filter( parent = outline )
		posts = Post.objects.filter( feed__in = feeds ).order_by( '-pubDate' )
	return render( request, 'feedreader/outline.html', { 
		'outline_list': main_navigation( request ), 
		'outline': outline,
		'posts': posts
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

class PostActionView(View):
	def post( self, request, post_id, action ):
		return self.getpost( request, post_id, action, request.POST )
	def get( self, request, post_id, action ):
		return self.getpost( request, post_id, action, request.GET )

	def getpost( self, request, post_id, action, params ):
		try:
			post = Post.objects.get( pk = post_id )
		except Post.DoesNotExist:
			raise Http404
		try:
			user_post = UserPost.objects.get( user = request.user, post = post )
		except UserPost.DoesNotExist:
			user_post = UserPost( user = request.user, post = post )
		state = None
		if 'state' in params:
			state = bool( int( params['state'] ) )
		if action in ( 'read', ):
			if state != None:
				setattr( user_post, action, state )
				user_post.save()
			return HttpResponse( simplejson.dumps( { 'caption': 'Result', 'message': 'OK', 'error': False } ), mimetype='application/json' )
		raise Http404
