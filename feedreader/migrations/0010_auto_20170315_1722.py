# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-15 17:22
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feedreader', '0009_auto_20170315_1638'),
    ]

    operations = [
    	migrations.RenameModel('Outline', 'OldOutline'),
    ]
