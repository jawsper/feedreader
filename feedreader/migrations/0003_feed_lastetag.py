# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feedreader', '0002_auto_20141113_2108'),
    ]

    operations = [
        migrations.AddField(
            model_name='feed',
            name='lastETag',
            field=models.CharField(blank=True, null=True, max_length=100),
            preserve_default=True,
        ),
    ]
