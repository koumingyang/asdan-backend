# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-11-15 08:34
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0018_auto_20171115_1550'),
    ]

    operations = [
        migrations.RenameField(
            model_name='information',
            old_name='tradestate',
            new_name='tradetype',
        ),
        migrations.RemoveField(
            model_name='information',
            name='tradesucc',
        ),
    ]
