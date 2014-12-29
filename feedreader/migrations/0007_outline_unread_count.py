# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feedreader', '0006_auto_20141119_1516'),
    ]

    operations = [
        migrations.AddField(
            model_name='outline',
            name='unread_count',
            field=models.IntegerField(default=0, db_index=True),
            preserve_default=True,
        ),
    ]
