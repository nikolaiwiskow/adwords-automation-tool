# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-10-30 20:01
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('structure', '0004_tagtrigger'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Negatives',
            new_name='Negative',
        ),
    ]
