# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feedreader', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='guid',
            field=models.CharField(db_index=True, max_length=250),
            preserve_default=True,
        ),
    ]
