from rest_framework import serializers
from rest_framework_recursive.fields import RecursiveField

from feedreader.models import Outline

from .feed import FeedSerializer


class SingleOutlineSerializer(serializers.ModelSerializer):
    feed = FeedSerializer(read_only=True)

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


class OutlineSerializer(SingleOutlineSerializer):
    children = serializers.ListField(child=RecursiveField())

    class Meta:
        model = Outline
        fields = SingleOutlineSerializer.Meta.fields + ["children"]
