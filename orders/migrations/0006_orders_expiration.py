# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-12-04 05:42
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0005_auto_20171118_1552'),
    ]

    operations = [
        migrations.AddField(
            model_name='orders',
            name='expiration',
            field=models.DateField(blank=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
