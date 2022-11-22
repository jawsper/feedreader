# Generated by Django 3.2.16 on 2022-11-21 21:53

from django.db import migrations
from mptt.models import MPTTModelBase
from treebeard.mp_tree import MP_Node


def old_outline_to_dict(outline):
    data = {
        "user": outline.user.id,
        "title": outline.title,
        "sort_order_asc": outline.sort_order_asc,
        "show_only_new": outline.show_only_new,
        "folder_opened": outline.folder_opened,
        "unread_count": outline.unread_count,
    }
    if outline.feed:
        data["feed"] = outline.feed.id
    return {
        "data": data,
        "children": [old_outline_to_dict(node) for node in outline.get_children()],
    }


def move_oldoutline_to_outline(apps, schema_editor):
    OldOutline = apps.get_model("feedreader", "OldOutline")
    MPTTModelBase.register(OldOutline)

    NewOutline = apps.get_model("feedreader", "Outline")
    bases = list(NewOutline.__bases__)
    bases.insert(0, MP_Node)
    NewOutline.__bases__ = tuple(bases)

    root_nodes = [
        old_outline_to_dict(node)
        for node in OldOutline._tree_manager.get_cached_trees()
    ]
    NewOutline.load_bulk(root_nodes)


def remove_new_outline(apps, schema_editor):
    NewOutline = apps.get_model("feedreader", "Outline")
    NewOutline.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ("feedreader", "0018_outline"),
    ]

    operations = [
        migrations.RunPython(
            move_oldoutline_to_outline, remove_new_outline, elidable=True
        )
    ]
