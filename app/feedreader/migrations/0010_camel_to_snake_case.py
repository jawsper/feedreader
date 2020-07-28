# Generated by Django 2.2.9 on 2020-01-28 14:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feedreader', '0009_remove_feed_quirkfixnotxml'),
    ]

    operations = [
        migrations.RenameField(
            model_name='feed',
            old_name='faviconUrl',
            new_name='favicon_url',
        ),
        migrations.RenameField(
            model_name='feed',
            old_name='htmlUrl',
            new_name='html_url',
        ),
        migrations.RenameField(
            model_name='feed',
            old_name='lastETag',
            new_name='last_etag',
        ),
        migrations.RenameField(
            model_name='feed',
            old_name='lastPubDate',
            new_name='last_pub_date',
        ),
        migrations.RenameField(
            model_name='feed',
            old_name='lastStatus',
            new_name='last_status',
        ),
        migrations.RenameField(
            model_name='feed',
            old_name='lastUpdated',
            new_name='last_updated',
        ),
        migrations.RenameField(
            model_name='feed',
            old_name='xmlUrl',
            new_name='xml_url',
        ),
    ]