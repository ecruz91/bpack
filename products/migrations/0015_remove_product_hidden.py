# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-11-27 23:52
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0014_auto_20171127_1747'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='hidden',
        ),
    ]
