from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework.schemas import get_schema_view
from rest_framework_nested import routers

from feedreader import __version__
from .views.config import ConfigViewSet
from .views.feed import FeedViewSet
from .views.outlines import OutlinesViewSet
from .views.posts import (
    PostsViewSet,
    PostEditViewSet,
    AllPostsViewSet,
    StarredPostsViewSet,
)
from .views.unread_count import UnreadCountViewSet

router = DefaultRouter()
router.register("outlines", OutlinesViewSet, basename="outlines")
router.register("feed", FeedViewSet, basename="feed")
router.register("posts/all", AllPostsViewSet, basename="all")
router.register("posts/starred", StarredPostsViewSet, basename="starred")
router.register("posts", PostEditViewSet, basename="posts")
router.register("unread_counts", UnreadCountViewSet, basename="unread_counts")

outlines_router = routers.NestedSimpleRouter(router, r"outlines", lookup="outline")
outlines_router.register("posts", PostsViewSet, basename="outline-posts")


urlpatterns = [
    path("", include(router.urls)),
    path("", include(outlines_router.urls)),
    path(
        "config/", ConfigViewSet.as_view({"get": "retrieve", "patch": "partial_update"})
    ),
    path(
        "openapi",
        get_schema_view(
            title="Feedreader",
            description="Feedreader",
            version=__version__,
            public=True,
            permission_classes=[],
        ),
        name="openapi-schema",
    ),
]
