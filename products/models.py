# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
#from tinymce import models as tinymce_models
#from tinymce.models import HTMLField
#rom autoslug import AutoSlugField
#Pre_delete signal to delete files
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver
from django.core.validators import RegexValidator
from django.template.defaultfilters import slugify
from clients.models import Clients
U_CHOICES = (
    ('kgs', 'Kilogramos'),
    ('millar', 'Millar'),
)

class Product(models.Model):
	added_date = models.DateField(auto_now_add=True, blank=True, null=True, verbose_name='Fecha de Registro')
	updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de Actualización")
	pid = models.CharField(unique=True, max_length=100, blank=True, verbose_name='ID de Producto')
	product = models.CharField(max_length=200, verbose_name='Descripción del Producto', unique=True)
	qty = models.FloatField(verbose_name='Cantidad', blank=False)
	unity = models.CharField(max_length=10, choices=U_CHOICES, default='kgs', verbose_name='Unidad')
	Clientes = models.ManyToManyField(Clients, verbose_name='Clientes asociados a Producto')
    	hidden = models.CharField(max_length=200, null=True, blank=True)

	class Meta:
		ordering = ('-id',)
		default_permissions = ('add', 'change', 'delete', 'view')

	def __unicode__(self):
		return '%s - %s'%(self.pid ,self.product)
