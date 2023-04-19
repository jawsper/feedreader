from rest_framework import serializers

from feedreader.models import UserPost


class PostSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source="post.pk")
    link = serializers.CharField(source="post.link")
    author = serializers.CharField(source="post.author")
    title = serializers.CharField(source="post.display_title")
    feed_title = serializers.CharField(source="post.feed.display_title")
    pub_date = serializers.DateTimeField(source="post.pubDate")
    content = serializers.CharField(source="post.processed_content")

    class Meta:
        model = UserPost
        fields = [
            "id",
            "link",
            "author",
            "title",
            "feed_title",
            "pub_date",
            "content",
            "starred",
            "read",
        ]
