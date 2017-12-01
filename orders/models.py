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
from products.models import Product
from django.contrib.auth.models import User


class Orders(models.Model):
	added_date = models.DateField(auto_now_add=True, null=True, verbose_name='Fecha de Registro')
	updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de Actualización")
	order = models.CharField(max_length=100, unique=True, verbose_name='OC')
	bpid = models.CharField(max_length=100, unique=True, verbose_name='ID de Orden')
	lq = models.CharField(max_length=100, unique=True,  verbose_name='LEQ')
	product_name = models.CharField(max_length=100,verbose_name='Nombre de producto')
	client_name = models.CharField(max_length=100,verbose_name='Nombre de cliente')
	packer_name = models.CharField(max_length=100,verbose_name='Nombre de empacador')
	product = models.ForeignKey(Product, verbose_name='Escoge un producto')
	client = models.ForeignKey(Clients, verbose_name='Escoge a un cliente')
	packer = models.ForeignKey(User, verbose_name='Escoge un empacador')
	flag = models.CharField(max_length=1, default='0')

	def save(self, *args, **kwargs):
		self.client_name = self.client.NAME.upper()
		self.product_name = self.product.product.upper()
		self.packer_name = self.packer.get_full_name().upper()
		super(Orders, self).save(*args, **kwargs)


	class Meta:
		ordering = ('-id',)
		default_permissions = ('add', 'change', 'delete', 'view')
		verbose_name = 'Orden'
		verbose_name_plural = 'Ordenes'

	def __unicode__(self):
		return '%s'%(self.order)

class Pallets(models.Model):
	order = models.ForeignKey(Orders, verbose_name='Orden de Compra')
	name = models.CharField(blank = True, max_length = 35, verbose_name='Tarima')

	class Meta:
		ordering = ('-id',)
		default_permissions = ('add', 'change', 'delete', 'view')
		verbose_name = 'Tarima'
		verbose_name_plural = 'Tarimas'

	def __unicode__(self):
		return '%s'%(self.name)
