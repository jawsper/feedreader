# api0/outline.py
# Author: Jasper Seidel
# Date: 2013-06-24

from feedreader.models import Outline, Post, Feed, UserPost
from feedreader.functions import get_total_unread_count
from feedreader.functions.feeds import add_feed
from feedreader_api.functions import JsonResponseView
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

DEFAULT_SKIP = 0
DEFAULT_LIMIT = 20


class AddFeedView(JsonResponseView):
    def get_response(self, user, args):
        if 'url' not in args:
            return dict(success=False, message='No URL supplied.')
        result = add_feed(user, args['url'])
        return dict(success='outline_id' in result, result=result)


class GetUnreadCountView(JsonResponseView):
    def get_response(self, user, args):
        total = 0
        counts = {}
        if 'outline_id' in args:
            try:
                outline = Outline.objects.get(pk=int(args['outline_id']))
            except Outline.DoesNotExist:
                return dict(success=False, message='Invalid outline ID.')

            counts[outline.id] = outline.unread_count
            if outline.parent:
                counts[outline.parent.id] = outline.parent.unread_count
            else:
                for child in Outline.objects.filter(parent=outline):
                    counts[child.id] = child.unread_count
            total = get_total_unread_count(user)
        else:
            for outline in Outline.objects.filter(user=user):
                counts[outline.id] = outline.unread_count
                if outline.feed:
                    total += outline.unread_count
        return dict(success=True, counts=counts, total=total)


class GetAllOutlinesView(LoginRequiredMixin, TemplateView):
    template_name = 'api0/navigation.html'
    content_type = 'application/json'

    def post(self, *args, **kwargs):
        return self.get(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nodes'] = Outline.objects.filter(user=self.request.user)
        return context


class GetAllPostsView(JsonResponseView):
    def get_response(self, user, args):
        skip = int(args.get('skip', DEFAULT_SKIP))
        limit = int(args.get('limit', DEFAULT_LIMIT))
        userposts = UserPost.objects.filter(user=user).select_related()[skip:limit]
        return dict(posts=[up.toJsonDict() for up in userposts])


class GetStarredPostsView(JsonResponseView):
    def get_response(self, user, args):
        skip = int(args.get('skip', DEFAULT_SKIP))
        limit = int(args.get('limit', DEFAULT_LIMIT))
        userposts = UserPost.objects.filter(user=user, starred=True).select_related()[skip:limit]
        return dict(posts=[up.toJsonDict() for up in userposts])


class GetPostsView(JsonResponseView):
    def get_response(self, user, args):
        try:
            outline_id = args.get('outline', None)
            outline = Outline.objects.get(user=user, id=outline_id)
        except Outline.DoesNotExist:
            return dict(success=False, message='Outline does not exist.')

        sort_order = 'ASC' if outline.sort_order_asc else 'DESC'
        order_by = ('post__pubDate' if outline.sort_order_asc else '-post__pubDate', 'post_id')
        show_only_new = outline.show_only_new
        skip = int(args.get('skip', DEFAULT_SKIP))
        limit = int(args.get('limit', DEFAULT_LIMIT))

        params = {
            'user': user,
            'post__feed__in': outline.get_descendants(include_self=True).values_list('feed_id', flat=True)
        }

        if show_only_new:
            params['read'] = False

        posts_queryset = UserPost.objects.filter(**params).select_related('post', 'post__feed').order_by(*order_by)[skip:skip+limit]
        posts = [post.toJsonDict() for post in posts_queryset]

        return dict(
            success=True,
            title=outline.display_title,
            htmlUrl=outline.feed.htmlUrl if outline.feed else None,
            is_feed=bool(outline.feed),
            show_only_new=show_only_new,
            sort_order=sort_order,
            skip=skip,
            limit=limit,
            posts=posts,
            unread_count=outline.unread_count
        )


class OutlineGetDataView(JsonResponseView):
    def get_response(self, user, args):
        try:
            outline_id = args.get('outline', None)
            outline = Outline.objects.get(user=user, id=outline_id)
        except Outline.DoesNotExist:
            return dict(success=False, message='Outline does not exist.')

        sort_order = 'ASC' if outline.sort_order_asc else 'DESC'
        show_only_new = outline.show_only_new

        return dict(
            success=True,
            title=outline.feed.title if outline.feed else outline.title,
            show_only_new=show_only_new,
            sort_order=sort_order,
            unread_count=outline.unread_count
        )


class OutlineSetView(JsonResponseView):
    def get_response(self, user, args):
        action_to_field = {
            'sort_order': 'sort_order_asc',
            'show_only_new': 'show_only_new',
            'folder_opened': 'folder_opened'
        }

        try:
            outline_id = args.get('outline', None)
            outline = Outline.objects.get(user=user, id=outline_id)
        except Outline.DoesNotExist:
            return dict(success=False, message='Outline does not exist.')

        if 'action' not in args:
            return dict(success=False, error='ERROR: action not set')

        if args['action'] not in action_to_field:
            return dict(success=False, error='ERROR: invalid action')

        if 'value' in args and args['value'] in ('0', '1'):
            value = args['value'] == '1'
        else:
            value = 'toggle'

        field = action_to_field[args['action']]
        if value == 'toggle':
            value = not getattr(outline, field)
        setattr(outline, field, value)

        outline.save()

        return dict(success=True, message='OK')


class OutlineMarkAsReadView(JsonResponseView):
    def get_response(self, user, args):
        try:
            outline_id = args.get('outline', None)
            outline = Outline.objects.get(user=user, id=outline_id)
        except Outline.DoesNotExist:
            return dict(success=False, message='Outline does not exist.')

        if outline.feed:
            posts = Post.objects.filter(feed=outline.feed)
        else:
            feed_ids = Outline.objects.filter(parent=outline).values_list('feed', flat=True)
            feeds = Feed.objects.filter(pk__in=feed_ids)
            posts = Post.objects.filter(feed__in=feeds)
        post_count = change_count = 0
        for post in posts:
            post_count += 1
            try:
                u = UserPost.objects.get(user=user, post=post)
            except UserPost.DoesNotExist:
                u = UserPost(user=user, post=post)
            if not u.id or not u.read:
                u.read = True
                u.save()
                change_count += 1
        return dict(success=True, post_count=post_count, change_count=change_count)
