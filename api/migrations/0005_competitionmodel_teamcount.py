# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-10-26 07:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_auto_20171026_1419'),
    ]

    operations = [
        migrations.AddField(
            model_name='competitionmodel',
            name='teamCount',
            field=models.IntegerField(null=True),
        ),
    ]
