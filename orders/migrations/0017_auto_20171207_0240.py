# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-12-07 08:40
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0016_auto_20171206_1915'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='pallets',
            options={'default_permissions': ('add', 'change', 'delete', 'view'), 'ordering': ('id',), 'verbose_name': 'Tarima', 'verbose_name_plural': 'Tarimas'},
        ),
        migrations.RemoveField(
            model_name='drop_number',
            name='pallet',
        ),
    ]
