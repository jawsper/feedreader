from rest_framework import serializers

from feedreader.models import Feed


class FeedSerializer(serializers.ModelSerializer):
    icon = serializers.CharField(read_only=True)

    class Meta:
        model = Feed
        fields = ["id", "title", "html_url", "is_nsfw", "icon"]


class NewFeedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feed
        fields = ["xml_url"]
