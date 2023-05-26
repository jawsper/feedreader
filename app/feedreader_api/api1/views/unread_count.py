from rest_framework import viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from feedreader.functions import get_total_unread_count
from feedreader.models import Outline

from ..serializers.unread_count import UnreadCountSerializer


class UnreadCountViewSet(viewsets.GenericViewSet):
    serializer_class = UnreadCountSerializer

    def list(self, *args, **kwargs):
        data = {
            "counts": {
                outline.id: outline.unread_count
                for outline in Outline.objects.filter(user=self.request.user)
            },
            "total": get_total_unread_count(self.request.user),
        }
        serializer = self.get_serializer(data)
        return Response(serializer.data)

    def retrieve(self, *args, pk: int):
        queryset = Outline.objects.filter(user=self.request.user, pk=pk)
        outline = get_object_or_404(queryset)

        counts = {}

        for ancestor in outline.get_ancestors():
            counts[ancestor.id] = ancestor.unread_count
        counts[outline.id] = outline.unread_count
        for descendant in outline.get_descendants():
            counts[descendant.id] = descendant.unread_count

        data = {"counts": counts, "total": get_total_unread_count(self.request.user)}
        serializer = self.get_serializer(data)
        return Response(serializer.data)
