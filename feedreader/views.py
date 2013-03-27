# Create your views here.

from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from feedreader.models import Outline, Feed, Post

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

def feed_favicon( request, feed_id ):
	import urlparse, urllib2, re
	
	feed = Feed.objects.get( pk = feed_id )
	if feed.faviconUrl:
		return HttpResponseRedirect( feed.faviconUrl )
	p_url = urlparse.urlparse( feed.htmlUrl )
	try:
		data = urllib2.urlopen( urllib2.Request( feed.htmlUrl, headers={'User-Agent': 'Chrome'} ) ).read()
		matches = re.findall( '<link ([^>]+)>', data )
		for match in matches:
			if re.search( 'rel="(shortcut )?icon"', match ):
				m = re.search( 'href="([^"]+)"', match )
				if not m:
					continue
				favicon_url = m.groups(1)[0]
				p_favicon_url = urlparse.urlparse( favicon_url )
				if not p_favicon_url.hostname:
					favicon_url = urlparse.urlunparse( p_url[0:2] + p_favicon_url[2:] )
				try:
					favicon = urllib2.urlopen( urllib2.Request( favicon_url, headers={'User-Agent': 'Chrome'} ) ).read()
					if favicon:
						feed.faviconUrl = favicon_url
						feed.save()
						return HttpResponseRedirect( feed.faviconUrl )
				except:
					pass
		favicon_url = '{0}://{1}/favicon.ico'.format( p_url[0], p_url[1] )
		try:
			favicon = urllib2.urlopen( urllib2.Request( favicon_url, headers={'User-Agent': 'Chrome'} ) ).read()
			if favicon:
				feed.faviconUrl = favicon_url
				feed.save()
				return HttpResponseRedirect( feed.faviconUrl )
		except:
			pass
	except:
		pass
	return HttpResponse( open( '/home/jasper/favicon.ico', 'r' ).read(), content_type = 'image/png' )
