# functions.py
# Author: Jasper Seidel
# Date: 2013-06-24

from django.http import HttpResponse
from django.db import connection
from django.utils.timezone import utc
from feedreader.models import Outline, UserToken

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
