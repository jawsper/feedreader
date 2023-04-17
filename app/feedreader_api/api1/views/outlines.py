from rest_framework import viewsets

from feedreader.models import Outline
from ..serializers.outline import OutlineSerializer


class OutlinesViewSet(viewsets.ReadOnlyModelViewSet):
    def get_queryset(self):
        return (
            Outline.objects.filter(user=self.request.user)
            .select_related("feed")
            .prefetch_related("feed")
            .get_cached_trees()
        )

    serializer_class = OutlineSerializer
