# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-12-07 01:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0015_auto_20171206_1853'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rolls',
            name='roll_name',
            field=models.PositiveIntegerField(verbose_name='N\xfamero de Rollo'),
        ),
    ]
