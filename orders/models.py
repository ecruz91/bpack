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
	product_name = models.CharField(max_length=100,verbose_name='Nombre de producto', blank=True, null=True)
	client_name = models.CharField(max_length=100,verbose_name='Nombre de cliente', blank=True, null=True)
	packer_name = models.CharField(max_length=100,verbose_name='Nombre de empacador', blank=True, null=True)
	product = models.ForeignKey(Product,blank=True, null=True, verbose_name='Escoge un producto', on_delete=models.SET_NULL)
	client = models.ForeignKey(Clients, blank=True, null=True, verbose_name='Escoge a un cliente', on_delete=models.SET_NULL)
	packer = models.ForeignKey(User, blank=True, null=True, verbose_name='Escoge un empacador', on_delete=models.SET_NULL)
	flag = models.CharField(max_length=1, default='0')
	expiration = models.DateField(verbose_name='Caducidad', blank=True,  null=True)

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
	weight = models.FloatField(verbose_name='Peso de Rollos',blank=False, default=0)
	pallet_weight = models.FloatField(verbose_name='Peso de Tarima', default=0)
	class Meta:
		ordering = ('-id',)
		default_permissions = ('add', 'change', 'delete', 'view')
		verbose_name = 'Tarima'
		verbose_name_plural = 'Tarimas'

	def __unicode__(self):
		return '%s'%(self.name)

	def save(self, *args,**kwargs):
		print 'Pallets'
		super(Pallets, self).save(*args, **kwargs)


class Rolls(models.Model):
	order = models.ForeignKey(Orders, verbose_name='Orden de Compra')
	roll_name = models.PositiveIntegerField(verbose_name='Número de Rollo')
	total_weight = models.FloatField(verbose_name='Sumatoria de Peso', blank=False, default=0)
	def save(self, *args,**kwargs):
		print 'saving Rolls'
		super(Rolls, self).save(*args, **kwargs)

	def __unicode__(self):
		return '%s - %sA'%(self.order.order,self.roll_name)

class Drops(models.Model):
	pallet = models.ForeignKey(Pallets, verbose_name='Lista Asociada')
	roll = models.ForeignKey(Rolls, verbose_name='Rollo')
	serie = models.CharField(verbose_name='Serie', max_length=1)
	total_weight = models.FloatField(verbose_name='Peso de la Serie',blank=False, default=0)
	def save(self, *args,**kwargs):
		print 'saving drops'
		super(Drops, self).save(*args,**kwargs)

class Drop_Number(models.Model):
	pallet = models.ForeignKey(Pallets, verbose_name='Tarima Asignada')
	drop = models.ForeignKey(Drops, verbose_name='Serie de Bajada')
	weight = models.FloatField(verbose_name='Peso de la Bajada',blank=False, default=0)
	def save(self,*args,**kwargs):
		self.pallet = self.drop.palled.id
		print 'saving drops'
		supder(Drop_Number)
		