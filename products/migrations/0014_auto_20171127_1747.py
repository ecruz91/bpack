# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-11-27 23:47
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0013_auto_20171127_1729'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='hidden',
            field=models.CharField(blank=True, default=django.utils.timezone.now, max_length=200),
            preserve_default=False,
        ),
    ]
