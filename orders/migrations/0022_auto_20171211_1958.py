# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-12-12 01:58
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0021_auto_20171209_1659'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='drop_number',
            options={'ordering': ('drop__roll__roll_name', 'drop__serie', 'drop_name')},
        ),
    ]
