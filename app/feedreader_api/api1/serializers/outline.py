from rest_framework import serializers
from rest_framework_recursive.fields import RecursiveField

from feedreader.models import Outline

from .feed import FeedSerializer


class SingleOutlineSerializer(serializers.ModelSerializer):
    title = serializers.CharField(read_only=True)
    feed = FeedSerializer(read_only=True)
    unread_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Outline
        fields = [
            "id",
            "title",
            "feed",
            "sort_order_asc",
            "show_only_new",
            "folder_opened",
            "unread_count",
        ]


class OutlineSerializer(serializers.ModelSerializer):
    feed = FeedSerializer(read_only=True)
    children = serializers.ListField(child=RecursiveField())

    class Meta:
        model = Outline
        fields = [
            "id",
            "title",
            "feed",
            "sort_order_asc",
            "show_only_new",
            "folder_opened",
            "unread_count",
            "children",
        ]
