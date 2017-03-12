# api0/post.py
# Author: Jasper Seidel
# Date: 2013-06-24

from django.db.models import F

from feedreader.models import Outline, Post, UserPost
from feedreader_api.functions import JsonResponseView

def _find_post_outline(userpost):
    user, post = userpost.user, userpost.post
    return Outline.objects.get(user=user, feed=post.feed)


def _update_unread_count_cascade(outline, num):
    outline.update(unread_count=F('unread_count') + num)
    if outline.parent:
        _update_unread_count_cascade(outline.parent, num)


def _update_unread_count(userpost, num):
    outline = _find_post_outline(userpost)
    if not outline:
        return
    _update_unread_count_cascade(outline, num)


class PostActionView(JsonResponseView):
    def get_response(self, user, args):
        try:
            post_id = args.get('post', None)
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return {'success': False, 'caption': 'Error', 'message': 'Post not found.'}

        action = args.get('action', None)
        state = args.get('state', None)
        try:
            state = bool(int(state))
        except ValueError:
            state = None
        if action not in ('starred', 'read') or state is None:
            return {'success': False, 'caption': 'Error', 'message': 'Invalid parameters.'}

        try:
            user_post = UserPost.objects.get(user=user, post=post)
        except UserPost.DoesNotExist:
            user_post = UserPost(user=user, post=post)

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
            return {'success': True, 'caption': 'Result', 'message': result_message}

        return {'success': True, 'caption': 'Result', 'message': 'Post[{}].{} not changed'.format(post.id, action)}
