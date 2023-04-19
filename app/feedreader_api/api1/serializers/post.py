from rest_framework import serializers

from feedreader.models import UserPost


class PostSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source="post.pk", read_only=True)
    link = serializers.CharField(source="post.link", read_only=True)
    author = serializers.CharField(source="post.author", read_only=True)
    title = serializers.CharField(source="post.display_title", read_only=True)
    feed_title = serializers.CharField(source="post.feed.display_title", read_only=True)
    pub_date = serializers.DateTimeField(source="post.pubDate", read_only=True)
    content = serializers.CharField(source="post.processed_content", read_only=True)

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
