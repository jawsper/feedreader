from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework.schemas import get_schema_view

from feedreader import __version__
from .views.outlines import OutlinesViewSet

router = DefaultRouter()
router.register(r"outlines", OutlinesViewSet, basename="outlines")

urlpatterns = [
    path("", include(router.urls)),
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
