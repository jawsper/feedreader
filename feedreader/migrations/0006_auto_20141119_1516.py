# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feedreader', '0005_auto_20141119_1355'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feed',
            name='title',
            field=models.CharField(max_length=500),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='outline',
            name='sort_position',
            field=models.IntegerField(blank=True, db_index=True, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='outline',
            name='title',
            field=models.CharField(db_index=True, max_length=500),
            preserve_default=True,
        ),
    ]
