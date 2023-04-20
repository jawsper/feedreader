from rest_framework import mixins, viewsets

from feedreader.functions.feeds import add_feed
from ..serializers.feed import NewFeedSerializer


class FeedViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = NewFeedSerializer

    def perform_create(self, serializer: NewFeedSerializer):
        feed_xml_url = serializer.data["xml_url"]
        add_feed(self.request.user, feed_xml_url)
