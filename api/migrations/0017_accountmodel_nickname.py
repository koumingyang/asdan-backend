# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-11-14 14:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0016_machinemodel_lock'),
    ]

    operations = [
        migrations.AddField(
            model_name='accountmodel',
            name='nickname',
            field=models.CharField(max_length=30, null=True),
        ),
    ]
