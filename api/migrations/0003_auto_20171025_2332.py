# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-10-25 15:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20171025_2329'),
    ]

    operations = [
        migrations.AlterField(
            model_name='competitionmodel',
            name='teams',
            field=models.ManyToManyField(to='api.TeamModel'),
        ),
        migrations.AlterField(
            model_name='teammodel',
            name='accounts',
            field=models.ManyToManyField(to='api.AccountModel'),
        ),
        migrations.AlterField(
            model_name='teammodel',
            name='machines',
            field=models.ManyToManyField(to='api.MachineModel'),
        ),
    ]
