# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-16 09:50
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feedreader', '0010_auto_20170315_1722'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='TreeOutline',
            new_name='Outline',
        ),
    ]
