# Generated by Django 4.2.2 on 2023-06-23 13:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("feedreader", "0021_alter_outline_user"),
    ]

    operations = [
        migrations.AlterField(
            model_name="userconfig",
            name="user",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="user_config",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]