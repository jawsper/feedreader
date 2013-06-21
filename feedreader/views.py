# Create your views here.

from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.views.generic.base import View
from django.core import serializers
from django.db import connection, transaction

from feedreader.models import Outline, Feed, Post, UserPost, ConfigStore

import json
import urllib2, urlparse
from PIL import Image
from StringIO import StringIO

def outline_to_dict_with_children( outline ):
	return {
		'id': outline.id,
		'title': outline.title,
		'feed_id': outline.feed.id if outline.feed else None,
		'children': [ outline_to_dict_with_children( outline ) for outline in Outline.objects.filter( parent_id = outline.id ) ],
	}
	
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

def main_navigation( request ):
	return [ outline_to_dict_with_children( outline ) for outline in Outline.objects.filter( parent_id = None, user = request.user.id ) ]

#def login( request ):
#	return render( request, 'feedreader/login.html' )

@login_required
def index( request ):
	return render( request, 'feedreader/index.html', { 'outline_list': main_navigation( request ) } )

@login_required
def get_option( request ):
	if 'keys[]' in request.POST:
		return HttpJsonResponse( options = { x.key: x.value for x in ConfigStore.objects.filter( user = request.user, key__in = request.POST.getlist( 'keys[]' ) ) } )
	if not 'key' in request.POST:
		return HttpJsonResponse( error = 'no key' )
	data = ConfigStore.objects.get( user = request.user, key = request.POST['key'] )
	if not data:
		return HttpJsonResponse()
	return HttpJsonResponse( key = data.key, value = data.value )

@login_required
def set_option( request ):
	if len( request.POST ) == 0:
		return HttpResponse( 'ERROR' )
	for key, value in request.POST.iteritems():
		ConfigStore( user = request.user, key = key, value = value ).save()
	return HttpResponse( 'OK' )

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
	
class HttpJsonResponse( HttpResponse ):
	def __init__( self, data = None, **kwargs ):
		HttpResponse.__init__( self, json.dumps( data if data else kwargs ), content_type = 'application/json' )
	
@login_required
def get_posts( request, outline_id ):
	try:
		outline = Outline.objects.get( pk = outline_id, user = request.user.id )
	except Outline.DoesNotExist:
		return HttpJsonResponse()
	
	sort_order = 'ASC' if outline.sort_order_asc else 'DESC'
	show_only_new = outline.show_only_new
	skip = int( request.POST['skip'] ) if 'skip' in request.POST else 0
	limit = 20
	
	if show_only_new:
		query_user_post_where = ' and ( UserPost.read is null or UserPost.read = 0 ) '
	else:
		query_user_post_where = ''
	
	if outline.feed:
		posts = Post.objects.raw(
		'select Post.*, UserPost.read ' +
		'from feedreader_post Post left outer join feedreader_userpost UserPost on ( Post.id = UserPost.post_id and UserPost.user_id = %s ) ' +
		'where Post.feed_id = %s ' + query_user_post_where + ' ' +
		'order by Post.pubDate ' + sort_order + ' ' +
		'LIMIT %s,%s', [ request.user.id, outline.feed.id, skip, limit ] )
	else:
		posts = Post.objects.raw(
		'select Post.*, UserPost.read ' +
		'from feedreader_post Post left outer join feedreader_userpost UserPost on ( Post.id = UserPost.post_id and UserPost.user_id = %s ) ' +
		'where Post.feed_id in ( select feed_id from feedreader_outline where parent_id = %s ) ' + query_user_post_where + ' ' +
		'order by Post.pubDate ' + sort_order + ' ' +
		'LIMIT %s,%s', [ request.user.id, outline.id, skip, limit ] )
	
	return HttpJsonResponse(
		title = outline.feed.title if outline.feed else outline.title,
		htmlUrl = outline.feed.htmlUrl if outline.feed else None,
		is_feed = bool( outline.feed ),
		show_only_new = show_only_new,
		sort_order = sort_order,
		skip = skip,
		limit = limit,
		posts = [ post.toJsonDict() for post in posts ],
		unread_count = get_unread_count( request.user, outline )
	)

@login_required
def get_outline_data( request, outline_id ):
	try:
		outline = Outline.objects.get( pk = outline_id, user = request.user.id )
	except Outline.DoesNotExist:
		return HttpJsonResponse()
	
	sort_order = 'ASC' if outline.sort_order_asc else 'DESC'
	show_only_new = outline.show_only_new
	
	return HttpJsonResponse( title = outline.feed.title if outline.feed else outline.title, show_only_new = show_only_new, sort_order = sort_order, unread_count = get_unread_count( request.user, outline ) )
	
@login_required
def outline_set( request, outline_id ):
	try:
		outline = Outline.objects.get( pk = outline_id, user = request.user.id )
	except Outline.DoesNotExist:
		return HttpResponse( 'ERROR' )
	
	if len( request.POST ) == 0 or 'action' not in request.POST:
		return HttpResponse( 'ERROR' )
	
	if request.POST['action'] not in ( 'sort_order', 'show_only_new' ):
		return HttpResponse( 'ERROR' )
	
	if 'value' in request.POST and request.POST['value'] in ( '0', '1' ):
		value = bool( request.POST['value'] )
	else:
		value = 'toggle'
	
	if request.POST['action'] == 'sort_order':
		if value == 'toggle':
			value = not outline.sort_order_asc
		outline.sort_order_asc = value
	elif request.POST['action'] == 'show_only_new':
		if value == 'toggle':
			value = not outline.show_only_new
		outline.show_only_new = value
	else:
		return HttpResponse( 'ERROR' )
		
	outline.save()
	
	return HttpResponse( 'OK' )

@login_required
@transaction.commit_manually
def outline_mark_as_read( request, outline_id ):
	try:
		outline = Outline.objects.get( pk = outline_id, user = request.user.id )
	except Outline.DoesNotExist:
		return HttpResponse( 'ERROR' )

	cursor = connection.cursor()
	if outline.feed:
		cursor.execute( 'insert ignore into `feedreader_userpost` ( `user_id`, `post_id` ) select %s, `id` from `feedreader_post` where `feed_id` = %s', [ request.user.id, outline.feed.id ] )
		cursor.execute( 'update `feedreader_userpost` set `read` = 1 where `user_id` = %s and `post_id` in ( select `id` from `feedreader_post` where `feed_id` = %s )', [ request.user.id, outline.feed.id ] )
	else:
		cursor.execute( 'insert ignore into `feedreader_userpost` ( `user_id`, `post_id` ) select %s, `id` from `feedreader_post` where `feed_id` in ( select `feed_id` from `feedreader_outline` where `parent_id` = %s )', [ request.user.id, outline.id ] )
		cursor.execute( 'update `feedreader_userpost` set `read` = 1 where `user_id` = %s and `post_id` in ( select `id` from `feedreader_post` where `feed_id` in ( select `feed_id` from `feedreader_outline` where `parent_id` = %s ) )', [ request.user.id, outline.id ] )
	cursor.close()

	transaction.commit()

	return HttpResponse( 'OK' )
	
@login_required
def get_unread_counts( request ):
	counts = { outline.id: get_unread_count( request.user, outline ) for outline in Outline.objects.filter( user = request.user ) }
	total = 0
	for outline in Outline.objects.filter( user = request.user, feed__isnull = False ):
		total += counts[ outline.id ]
	return HttpJsonResponse( counts = counts, total = total )

@login_required
def api0( request, action ):
	return HttpResponse( 'OK' )

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
			return HttpJsonResponse( caption = 'Result', message = 'Post {} marked as {}'.format( post_id, 'read' if state else 'unread' ), error = False )
		raise Http404
