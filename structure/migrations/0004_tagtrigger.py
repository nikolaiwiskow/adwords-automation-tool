# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-10-30 20:01
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('structure', '0003_countrycode_negatives_tag'),
    ]

    operations = [
        migrations.CreateModel(
            name='TagTrigger',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('trigger_word', models.CharField(max_length=200)),
                ('country_code', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='structure.CountryCode')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='structure.Tag')),
            ],
        ),
    ]