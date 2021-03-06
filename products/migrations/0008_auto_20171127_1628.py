# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-11-27 22:28
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0007_remove_product_hidden'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='hidden',
            field=models.CharField(default=django.utils.timezone.now, max_length=200, null=True, verbose_name='Descripci\xf3n del Producto'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='product',
            name='pid',
            field=models.CharField(blank=True, max_length=100, unique=True, verbose_name='ID de Producto'),
        ),
    ]
