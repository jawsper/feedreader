# Generated by Django 3.2.16 on 2022-11-21 21:27

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("feedreader", "0015_feed_errored_since"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="Outline",
            new_name="OldOutline",
        ),
    ]
