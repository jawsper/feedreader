from django.contrib.auth.models import User
from django.db import models

from mptt.models import MPTTModel, TreeForeignKey

from .display_title import DisplayTitleMixIn
from .feed import Feed


class Outline(MPTTModel, DisplayTitleMixIn):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="outlines")
    parent = TreeForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="children",
        db_index=True,
    )
    title = models.CharField(max_length=500, db_index=True)
    feed = models.ForeignKey(Feed, on_delete=models.CASCADE, null=True, blank=True)
    sort_order_asc = models.BooleanField(default=True)
    show_only_new = models.BooleanField(default=True)
    folder_opened = models.BooleanField(default=True)
    unread_count = models.IntegerField(default=0, db_index=True)

    def __str__(self):
        return self.display_title

    @property
    def icon(self):
        from feedreader.functions import ensure_https_url

        if self.feed:
            return ensure_https_url(self.feed.favicon_url)

    def to_dict(self, include_children=True):
        outline = {
            "id": self.pk,
            "title": self.title,
            "unread_count": self.unread_count,
            "feed_id": self.feed_id,
            "icon": self.feed.favicon.url
            if self.feed_id and self.feed.favicon
            else None,
            "folder_opened": self.folder_opened,
        }
        if include_children:
            outline["children"] = [node.to_dict() for node in self.get_children()]
        return outline
