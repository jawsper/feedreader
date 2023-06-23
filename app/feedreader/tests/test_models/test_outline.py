from django.contrib.auth import get_user_model
from django.test import TestCase

from feedreader.models import Outline


class OutlineTestCase(TestCase):
    def setUp(self):
        user = get_user_model().objects.create()
        o1 = Outline.add_root(title="o1", user=user)
        o2 = o1.add_child(title="o2", user=user)
        o2.add_child(title="o3", user=user)

    def test_outline_get_ancestors(self):
        o1 = Outline.objects.get(title="o1")
        o2 = Outline.objects.get(title="o2")
        o3 = Outline.objects.get(title="o3")
        assert o1.is_root()
        assert o3.is_leaf()
        assert o2.is_child_of(o1)
        assert o3.is_child_of(o2)
        assert o3.is_descendant_of(o1)

        assert (
            len(o3.get_ancestors()) == 2
        ), "Get ancestors of child of child of root returns two objects"
        assert (
            len(o3.get_ancestors(include_self=True)) == 3
        ), "Get ancestors of child of child of root with self returns three objects"

        assert (
            len(o2.get_ancestors()) == 1
        ), "Get ancestors of child of root returns one object"
        assert (
            len(o2.get_ancestors(include_self=True)) == 2
        ), "Get ancestors of child of root with self returns two objects"

        assert len(o1.get_ancestors()) == 0, "Get ancestors of root returns nothing"
        assert (
            len(o1.get_ancestors(include_self=True)) == 1
        ), "Get ancestors with self of root returns one object"
