# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-10-30 20:08
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('structure', '0005_auto_20171030_2101'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Tag',
            new_name='TopicTag',
        ),
        migrations.RenameModel(
            old_name='TagTrigger',
            new_name='TopicTagTrigger',
        ),
    ]
