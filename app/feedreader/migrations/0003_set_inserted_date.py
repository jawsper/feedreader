# Generated by Django 2.0 on 2018-02-04 08:45

from django.db import migrations, models


def populate_dates(apps, schema_editor):
    Post = apps.get_model("feedreader", "Post")
    db_alias = schema_editor.connection.alias
    Post.objects.using(db_alias).update(inserted_date=models.F("pubDate"))


class Migration(migrations.Migration):

    dependencies = [
        ("feedreader", "0002_add_inserted_date"),
    ]

    operations = [
        migrations.RunPython(populate_dates),
    ]
