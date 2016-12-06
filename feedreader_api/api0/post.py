# api0/post.py
# Author: Jasper Seidel
# Date: 2013-06-24

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from feedreader.functions import HttpJsonResponse
from feedreader.models import Outline, Post, UserPost

def _find_post_outline(userpost):
    user, post = userpost.user, userpost.post
    return Outline.objects.get(user=user, feed=post.feed)

def _update_unread_count_cascade(outline, num):
    # print(outline, num)
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
        post_id = request.POST.get('post', None)
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return JsonResponse({'error': True, 'caption': 'Error', 'message': 'Post not found.'})

    action = request.POST.get('action', None)
    state = request.POST.get('state', None)
    try:
        state = bool(int(state))
    except ValueError:
        state = None
    if action not in ('starred', 'read') or state is None:
        return JsonResponse({'error': True, 'caption': 'Error', 'message': 'Invalid parameters.'})

    try:
        user_post = UserPost.objects.get(user=request.user, post=post)
    except UserPost.DoesNotExist:
        user_post = UserPost(user=request.user, post=post)

    changed = False
    if user_post.pk is None:
        changed = True
    else:
        current_value = getattr(user_post, action)
        if current_value != state:
            changed = True

    if changed:
        setattr(user_post, action, state)
        user_post.save()
        if action == 'read':
            _update_unread_count(user_post, -1 if state else +1)

        result_message = 'Post {} marked as {}'.format(post_id, action if state else 'not ' + action)
        return JsonResponse({'error': False, 'caption': 'Result', 'message': result_message})

    return JsonResponse({'error': False, 'caption': 'Result', 'message': 'Post[{}].{} not changed'.format(post.id, action)})
