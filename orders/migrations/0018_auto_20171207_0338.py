# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-12-07 09:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0017_auto_20171207_0240'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='drops',
            options={'ordering': ('serie',)},
        ),
        migrations.AddField(
            model_name='drop_number',
            name='drop_name',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='N\xfamero de Bajada'),
        ),
    ]
