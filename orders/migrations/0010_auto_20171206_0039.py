# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-12-06 06:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0009_auto_20171206_0013'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='client_name',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Nombre de cliente'),
        ),
        migrations.AlterField(
            model_name='orders',
            name='packer_name',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Nombre de empacador'),
        ),
        migrations.AlterField(
            model_name='orders',
            name='product_name',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Nombre de producto'),
        ),
    ]
