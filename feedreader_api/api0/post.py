# api0/post.py
# Author: Jasper Seidel
# Date: 2013-06-24

from django.contrib.auth.decorators import login_required
from feedreader.functions import HttpJsonResponse
from feedreader.models import Outline, Post, UserPost

def _find_post_outline(userpost):
    user, post = userpost.user, userpost.post
    return Outline.objects.get(user=user, feed=post.feed)

def _update_unread_count_cascade(outline, num):
    print(outline, num)
    outline.unread_count += num
    outline.save()
    if outline.parent:
        _update_unread_count_cascade(outline.parent, num)

def _update_unread_count(userpost, num):
    outline = _find_post_outline(userpost)
    if not outline:
        return
    _update_unread_count_cascade(outline, num)

@login_required
def action(request):
    try:
        post_id = int(request.POST['post'])
        action = request.POST['action']
        post = Post.objects.get( pk = post_id )
    except Post.DoesNotExist:
        raise Http404
    except:
        raise Http404
        
    try:
        user_post = UserPost.objects.get( user = request.user, post = post )
    except UserPost.DoesNotExist:
        user_post = UserPost( user = request.user, post = post )
        
    params = request.POST

    state = None
    if 'state' in params:
        state = bool( int( params['state'] ) )
    if action in ( 'starred', 'read' ):
        if state != None:
            setattr( user_post, action, state )
            user_post.save()
        if action == 'read':
            _update_unread_count(user_post, -1 if state else +1)
        return HttpJsonResponse( caption = 'Result', message = 'Post {} marked as {}'.format( post_id, action if state else 'not ' + action ), error = False )
    raise Http404
