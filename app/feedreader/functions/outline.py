from django.db.models import F

from feedreader.models import Outline, UserPost


def _find_post_outline(userpost: UserPost) -> Outline:
    user, post = userpost.user, userpost.post
    return Outline.objects.get(user=user, feed=post.feed)


def update_userpost_unread_count(userpost: UserPost, num: int):
    outline = _find_post_outline(userpost)
    if outline:
        update_outline_unread_count(outline, num)


def update_outline_unread_count(outline: Outline, num: int):
    outlines = outline.get_ancestors(include_self=True)
    outlines.update(unread_count=F("unread_count") + num)
