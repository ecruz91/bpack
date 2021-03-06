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
import math
from django.db.models import Sum
from django.db.models.signals import post_delete

class Orders(models.Model):
	added_date = models.DateTimeField(auto_now_add=True, null=True, verbose_name='Fecha de Registro')
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
	qty = models.FloatField(verbose_name='Cantidad', blank=False,default=0)
	weight = models.FloatField(verbose_name='Cantidad', blank=False, default=0)
	delta_weight = models.FloatField(verbose_name='Diferencia de Peso', blank=False, default=0)


	def save(self, *args, **kwargs):
		qs = Pallets.objects.filter(order_id=self.id).aggregate(Sum('weight'))
		qs = qs['weight__sum']
		if qs is None:
			qs = 0
		self.weight = round(qs,2)
		self.delta_weight = round(self.weight - self.qty ,2)
		print 'saving'
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
	pallet_weight = models.FloatField(verbose_name='Peso de Tarima', default=14.5)
	class Meta:
		ordering = ('id',)
		default_permissions = ('add', 'change', 'delete', 'view')
		verbose_name = 'Tarima'
		verbose_name_plural = 'Tarimas'

	def __unicode__(self):
		return 'Lista de Empaque %s'%(self.name)

	def save(self, *args,**kwargs):
		qs = Drops.objects.filter(pallet_id=self.id).aggregate(Sum('total_weight'))
		qs = qs['total_weight__sum']
		if qs is None:
			qs = 0
		self.weight = round(qs,2)
		super(Pallets, self).save(*args, **kwargs)
		Orders.objects.get(pk=self.order_id).save()
	def delete(self,*args,**kwargs):
		super(Pallets, self).delete(*args,**kwargs)
		Orders.objects.get(pk=self.order_id).save()

class Rolls(models.Model):
	order = models.ForeignKey(Orders, verbose_name='Orden de Compra')
	roll_name = models.PositiveIntegerField(verbose_name='Número de Rollo')
	total_weight = models.FloatField(verbose_name='Sumatoria de Peso', blank=False, default=0)
	def save(self, *args,**kwargs):
		qs = Drops.objects.filter(roll_id=self.id).aggregate(Sum('total_weight'))
		qs = qs['total_weight__sum']
		if qs is None:
			qs = 0
		self.total_weight = qs
		super(Rolls, self).save(*args, **kwargs)

	def __unicode__(self):
		return '%s - %sA'%(self.order.order,self.roll_name)

class Drops(models.Model):
	pallet = models.ForeignKey(Pallets, verbose_name='Lista Asociada')
	roll = models.ForeignKey(Rolls, verbose_name='Rollo')
	serie = models.CharField(verbose_name='Serie', max_length=1)
	total_weight = models.FloatField(verbose_name='Peso de la Serie',blank=False, default=0)
	class Meta:
		ordering = ('serie',)

	def save(self, *args,**kwargs):
		self.serie = self.serie.upper()
		qs = Drop_Number.objects.filter(drop_id=self.id).aggregate(Sum('weight'))
		qs = qs['weight__sum']
		if qs is None:
			qs = 0
		self.total_weight = round(qs,2)
		super(Drops, self).save(*args,**kwargs)
		Rolls.objects.get(pk=self.roll.id).save()
		Pallets.objects.get(pk=self.pallet.id).save()
	def delete(self,*args,**kwargs):
		super(Drops,self).delete(*args,**kwargs)
		Rolls.objects.get(pk=self.roll.id).save()
		Pallets.objects.get(pk=self.pallet.id).save()
	def __unicode__(self):
		return 'Orden:%s, Bajadas:%sA-%s'%(self.roll.order.order,self.roll.roll_name,self.serie)


class Drop_Number(models.Model):
	drop = models.ForeignKey(Drops, verbose_name='Serie de Bajada')
	weight = models.FloatField(verbose_name='Peso de la Bajada',blank=False, default=0)
	drop_name = models.PositiveIntegerField(verbose_name='Número de Bajada', blank=True, null=True)
	def save(self,*args,**kwargs):
		super(Drop_Number,self).save(*args,**kwargs)
		Drops.objects.get(pk=self.drop.id).save()
	def delete(self,*args, **kwargs):
		super(Drop_Number, self).delete(*args,**kwargs)
		Drops.objects.get(pk=self.drop.id).save()
	class Meta:
		ordering = ('drop__roll__roll_name','drop__serie','drop_name',)
	def __unicode__(self):
		drop_name = "%02d" % (self.drop_name,)
		return '%sA-%s%s'%(self.drop.roll.roll_name,self.drop.serie,drop_name)


@receiver(post_delete, sender=Rolls)
def updating_pallets(sender, instance, **kwargs):
	object_list = Pallets.objects.filter(order_id=instance.order.id)
	for object in object_list:
		print object.id
		object.save()
