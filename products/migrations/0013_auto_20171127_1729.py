# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-11-27 23:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0012_auto_20171127_1652'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='hidden',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
