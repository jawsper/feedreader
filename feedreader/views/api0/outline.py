# api0/outline.py
# Author: Jasper Seidel
# Date: 2013-06-24

from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.db import connection, transaction
from feedreader.views import HttpJsonResponse, get_unread_count
from feedreader.models import Outline, Post

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
	action_to_field = \
	{
		'sort_order': 'sort_order_asc',
		'show_only_new': 'show_only_new',
		'folder_opened': 'folder_opened'
	}

	try:
		outline = Outline.objects.get( pk = outline_id, user = request.user.id )
	except Outline.DoesNotExist:
		return HttpResponse( 'ERROR: outline does not exist' )
	
	if len( request.POST ) == 0 or 'action' not in request.POST:
		return HttpResponse( 'ERROR: action not set' )
	
	if request.POST['action'] not in action_to_field:
		return HttpResponse( 'ERROR: invalid action' )
	
	if 'value' in request.POST and request.POST['value'] in ( '0', '1' ):
		value = bool( request.POST['value'] )
	else:
		value = 'toggle'
	
	field = action_to_field[ request.POST['action'] ]
	if value == 'toggle':
		value = not getattr( outline, field )
	setattr( outline, field, value )
		
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

	transaction.commit_unless_managed()

	return HttpResponse( 'OK' )
