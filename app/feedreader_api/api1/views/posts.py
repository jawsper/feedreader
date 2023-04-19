from rest_framework import viewsets, pagination

from feedreader.models import Outline, UserConfig, UserPost
from ..serializers.post import PostSerializer


class PostPagination(pagination.LimitOffsetPagination):
    default_limit = 10


class PostsViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PostSerializer
    pagination_class = PostPagination

    lookup_field = "post_id"

    def filter_queryset(self, queryset):
        return super().filter_queryset(queryset)

    def get_queryset(self):
        user = self.request.user

        # when using the post detail endpoint
        if self.lookup_field in self.kwargs:
            return UserPost.objects.filter(user=user).select_related(
                "post", "post__feed"
            )

        config, _ = UserConfig.objects.get_or_create(user=user)

        try:
            outline_id = self.kwargs["outline_pk"]
            outline = Outline.objects.only(
                "id", "numchild", "path", "depth", "show_only_new", "sort_order_asc"
            ).get(user=user, id=outline_id)
        except Outline.DoesNotExist:
            return UserPost.objects.none()

        feed_query = Outline.get_tree(outline)
        if not config.show_nsfw_feeds:
            feed_query = feed_query.filter(feed__is_nsfw=False)

        params = {
            "user": user,
            "post__feed__in": feed_query.values_list("feed_id", flat=True),
        }

        if outline.show_only_new:
            params["read"] = False

        posts_queryset = (
            UserPost.objects.filter(**params)
            .select_related("post", "post__feed")
            .order_by("post_id")
        )

        # sort_order = "ASC" if outline.sort_order_asc else "DESC"
        if not outline.sort_order_asc:
            posts_queryset = posts_queryset.reverse()

        return posts_queryset
