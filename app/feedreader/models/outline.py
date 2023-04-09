from typing import List, Optional, Self

from django.conf import settings
from django.db import models

from treebeard.mp_tree import MP_Node, MP_NodeManager, MP_NodeQuerySet, get_result_class

from .display_title import DisplayTitleMixIn
from .feed import Feed


class OutlineQueryset(MP_NodeQuerySet):
    def get_cached_trees(self):
        """Return top-most pages / roots.

        Each page will have its children stored in `_cached_children` attribute
        and its parent in `_cached_parent`. This avoids having to query the database.
        """

        top_nodes: List[Outline] = []
        path: List[Outline] = []

        def add_top_node(obj: Outline) -> None:
            top_nodes.append(obj)
            path.clear()

        def add_child(parent: Outline, obj: Outline) -> None:
            obj._cached_parent = parent
            parent._cached_children.append(obj)

        def is_child_of(child: Outline, parent: Outline) -> bool:
            """Return whether `child` is a sub page of `parent` without database query.

            `_get_children_path_interval` is an internal method of MP_Node.
            """
            return child.is_descendant_of(parent)

        obj: Outline
        for obj in self:
            obj._cached_children.clear()
            if obj.depth == self[0].depth:
                add_top_node(obj)
            else:
                while not is_child_of(obj, parent := path[-1]):
                    path.pop()
                add_child(parent, obj)

            if not obj.is_leaf():
                path.append(obj)

        return top_nodes


class OutlineManager(MP_NodeManager):
    def get_queryset(self):
        return OutlineQueryset(self.model).order_by("path")


class Outline(MP_Node, DisplayTitleMixIn):
    objects = OutlineManager()
    _cached_parent: Optional[Self] = None
    _cached_children: List[Self] = []

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="outlines"
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
    def children(self) -> List[Self]:
        if not self._cached_children:
            self._cached_children = list(self.get_children())
        return self._cached_children

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
            outline["children"] = [node.to_dict() for node in self.children]
        return outline

    def get_ancestors(self, include_self=False):
        if self.is_root():
            return get_result_class(self.__class__).objects.none()
        paths = [self.path[0:pos] for pos in range(0, len(self.path), self.steplen)[1:]]
        if include_self:
            paths.append(self.path)
        return (
            get_result_class(self.__class__)
            .objects.filter(path__in=paths)
            .order_by("depth")
        )
