# api0/outline.py
# Author: Jasper Seidel
# Date: 2013-06-24

from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.db import connection, transaction
from feedreader.functions import HttpJsonResponse, get_unread_count
from feedreader.models import Outline, Post, Feed, UserPost
import feedreader.functions as func
from feedreader.functions import main_navigation

@login_required
def add_feed( request ):
    if not 'url' in request.POST:
        return HttpJsonResponse( success = False, message = 'No URL supplied' )

    result = func.add_feed( request.user, request.POST['url'] )

    return HttpJsonResponse( success = 'outline_id' in result, result = result )

@login_required
def get_all_outlines( request ):
    return HttpJsonResponse( outlines = main_navigation( request ) )

@login_required
def get_all_posts(request):
    skip = int(request.POST['skip']) if 'skip' in request.POST else 0
    limit = int(request.POST['limit']) if 'limit' in request.POST else 20
    userposts = UserPost.objects.filter(user=request.user).select_related()[skip:limit]
    return HttpJsonResponse(posts=[up.toJsonDict() for up in userposts])

@login_required
def get_starred_posts(request):
    skip = int(request.POST['skip']) if 'skip' in request.POST else 0
    limit = int(request.POST['limit']) if 'limit' in request.POST else 20
    userposts = UserPost.objects.filter(user=request.user, starred=True).select_related()[skip:limit]
    return HttpJsonResponse(posts=[up.toJsonDict() for up in userposts])

def __get_outline(request):
    print '__check_outline_id'
    if 'outline' in request.POST:
        try:
            outline_id = int(request.POST['outline'])
            return Outline.objects.get( pk = outline_id, user = request.user.id )
        except Outline.DoesNotExist:
            raise Exception("Outline not found")
        except:
            raise Exception("Invalid outline id supplied")
    else:
        raise Exception("No outline id supplied")

@login_required
def get_posts(request):
    try:
        outline = __get_outline(request)
    except Exception as e:
        return HttpJsonResponse(error=e.message)

    sort_order = 'ASC' if outline.sort_order_asc else 'DESC'
    show_only_new = outline.show_only_new
    skip = int( request.POST['skip'] ) if 'skip' in request.POST else 0
    limit = int(request.POST['limit']) if 'limit' in request.POST else 20

    if show_only_new:
        query_user_post_where = ' and ( UserPost.read is null or UserPost.read = 0 ) '
    else:
        query_user_post_where = ''

    if outline.feed:
        posts = Post.objects.raw(
        'select Post.*, UserPost.starred, UserPost.read ' +
        'from feedreader_post Post left outer join feedreader_userpost UserPost on ( Post.id = UserPost.post_id and UserPost.user_id = %s ) ' +
        'where Post.feed_id = %s ' + query_user_post_where + ' ' +
        'order by Post.pubDate ' + sort_order + ' ' +
        'LIMIT %s,%s', [ request.user.id, outline.feed.id, skip, limit ] )
    else:
        posts = Post.objects.raw(
        'select Post.*, UserPost.starred, UserPost.read ' +
        'from feedreader_post Post left outer join feedreader_userpost UserPost on ( Post.id = UserPost.post_id and UserPost.user_id = %s ) ' +
        'where Post.feed_id in ( select feed_id from feedreader_outline where parent_id = %s ) ' + query_user_post_where + ' ' +
        'order by Post.pubDate ' + sort_order + ' ' +
        'LIMIT %s,%s', [ request.user.id, outline.id, skip, limit ] )

    return HttpJsonResponse(
        title = outline.feed.display_title if outline.feed else outline.display_title,
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
def get_outline_data(request):
    try:
        outline = __get_outline(request)
    except Exception as e:
        return HttpJsonResponse(error=e.message)

    sort_order = 'ASC' if outline.sort_order_asc else 'DESC'
    show_only_new = outline.show_only_new

    return HttpJsonResponse(
        title = outline.feed.title if outline.feed else outline.title,
        show_only_new = show_only_new,
        sort_order = sort_order,
        unread_count = get_unread_count( request.user, outline )
    )

@login_required
def outline_set( request ):
    action_to_field = \
    {
        'sort_order': 'sort_order_asc',
        'show_only_new': 'show_only_new',
        'folder_opened': 'folder_opened'
    }

    try:
        outline = __get_outline(request)
    except Exception as e:
        return HttpJsonResponse(error=e.message)

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

    return HttpJsonResponse(message='OK')

@login_required
def outline_mark_as_read( request ):
    try:
        outline = __get_outline(request)
    except Exception as e:
        return HttpJsonResponse(error=e.message)

    if outline.feed:
        posts = Post.objects.filter( feed = outline.feed )
    else:
        feed_ids = Outline.objects.filter( parent = outline ).values_list( 'feed', flat = True )
        feeds = Feed.objects.filter( pk__in = feed_ids )
        posts = Post.objects.filter( feed__in = feeds )
    post_count = change_count = 0
    for post in posts:
        post_count += 1
        try:
            u = UserPost.objects.get( user = request.user, post = post )
        except UserPost.DoesNotExist:
            u = UserPost( user = request.user, post = post )
        if not u.id or not u.read:
            u.read = True
            u.save()
            change_count += 1
    return HttpJsonResponse(post_count = post_count, change_count = change_count)

@login_required
@transaction.commit_manually
def outline_mark_as_read_old( request, outline_id ):
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
