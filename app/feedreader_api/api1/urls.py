from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework.schemas import get_schema_view
from rest_framework_nested import routers

from feedreader import __version__
from .views.outlines import OutlinesViewSet
from .views.posts import PostsViewSet

router = DefaultRouter()
router.register(r"outlines", OutlinesViewSet, basename="outlines")

outlines_router = routers.NestedSimpleRouter(router, r"outlines", lookup="outline")
outlines_router.register(r"posts", PostsViewSet, basename="outline-posts")

urlpatterns = [
    path("", include(router.urls)),
    path("", include(outlines_router.urls)),
    path(
        "openapi",
        get_schema_view(
            title="Feedreader",
            description="Feedreader",
            version=__version__,
        ),
        name="openapi-schema",
    ),
]
