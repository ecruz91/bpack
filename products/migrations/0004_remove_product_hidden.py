# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-11-27 22:24
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_auto_20171127_1623'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='hidden',
        ),
    ]
