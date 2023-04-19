from rest_framework import viewsets

from feedreader.models import Outline
from ..serializers.outline import OutlineSerializer, SingleOutlineSerializer


class OutlinesViewSet(viewsets.ReadOnlyModelViewSet):
    def get_queryset(self):
        qs = Outline.objects.filter(user=self.request.user).select_related("feed")
        if self.kwargs:
            return qs
        return qs.get_cached_trees()

    def get_serializer_class(self):
        if self.kwargs:
            return SingleOutlineSerializer
        return super().get_serializer_class()

    serializer_class = OutlineSerializer
