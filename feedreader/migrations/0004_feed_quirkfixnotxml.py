# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feedreader', '0003_feed_lastetag'),
    ]

    operations = [
        migrations.AddField(
            model_name='feed',
            name='quirkFixNotXml',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
