# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feedreader', '0004_feed_quirkfixnotxml'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userpost',
            name='read',
            field=models.BooleanField(default=False, db_index=True),
            preserve_default=True,
        ),
    ]
