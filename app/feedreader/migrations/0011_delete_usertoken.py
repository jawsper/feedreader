# Generated by Django 3.2.7 on 2021-10-11 11:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("feedreader", "0010_camel_to_snake_case"),
    ]

    operations = [
        migrations.DeleteModel(
            name="UserToken",
        ),
    ]
