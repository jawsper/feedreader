# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ConfigStore',
            fields=[
                ('key', models.CharField(primary_key=True, max_length=255, serialize=False)),
                ('value', models.CharField(max_length=255)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Feed',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('title', models.CharField(max_length=1000)),
                ('xmlUrl', models.CharField(max_length=1000)),
                ('htmlUrl', models.CharField(max_length=1000)),
                ('faviconUrl', models.CharField(max_length=1000, null=True, blank=True)),
                ('lastPubDate', models.DateTimeField(null=True, blank=True)),
                ('lastUpdated', models.DateTimeField(null=True, blank=True)),
                ('lastStatus', models.CharField(max_length=1000, null=True, blank=True)),
                ('disabled', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Outline',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('title', models.CharField(max_length=1000)),
                ('sort_position', models.IntegerField(null=True, blank=True)),
                ('sort_order_asc', models.BooleanField(default=True)),
                ('show_only_new', models.BooleanField(default=True)),
                ('folder_opened', models.BooleanField(default=True)),
                ('feed', models.ForeignKey(null=True, blank=True, to='feedreader.Feed')),
                ('parent', models.ForeignKey(null=True, blank=True, to='feedreader.Outline')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('title', models.CharField(max_length=1000)),
                ('link', models.CharField(max_length=1000)),
                ('category', models.CharField(max_length=1000, null=True, blank=True)),
                ('pubDate', models.DateTimeField()),
                ('guid', models.CharField(db_index=True, max_length=1000)),
                ('guid_is_permalink', models.BooleanField(default=False)),
                ('author', models.CharField(max_length=1000, null=True, blank=True)),
                ('content', models.TextField()),
                ('description', models.TextField()),
                ('feed', models.ForeignKey(to='feedreader.Feed')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserPost',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('starred', models.BooleanField(default=False)),
                ('read', models.BooleanField(default=False)),
                ('post', models.ForeignKey(to='feedreader.Post')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserToken',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('token', models.CharField(max_length=255)),
                ('expire', models.DateTimeField()),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='userpost',
            unique_together=set([('user', 'post')]),
        ),
        migrations.AlterUniqueTogether(
            name='configstore',
            unique_together=set([('key', 'user')]),
        ),
    ]
