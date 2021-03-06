# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-10-31 14:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_auto_20171031_1926'),
    ]

    operations = [
        migrations.CreateModel(
            name='Information',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=30)),
                ('description', models.CharField(max_length=100)),
                ('time', models.CharField(max_length=30)),
                ('compnum', models.IntegerField(null=True)),
                ('team1num', models.IntegerField(null=True)),
                ('team2num', models.IntegerField(null=True)),
                ('dmoney', models.IntegerField(null=True)),
                ('material', models.IntegerField(null=True)),
                ('dmaterial', models.IntegerField(null=True)),
                ('restmaterial1', models.IntegerField(null=True)),
                ('restmaterial2', models.IntegerField(null=True)),
                ('restmoney1', models.IntegerField(null=True)),
                ('restmoney2', models.IntegerField(null=True)),
            ],
        ),
        migrations.AddField(
            model_name='competitionmodel',
            name='turn',
            field=models.IntegerField(null=True),
        ),
    ]
