# -*- coding: utf-8
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Clients(models.Model):
	CID = models.CharField(blank = False, max_length = 6, unique=True, verbose_name="ID")
	NAME = models.CharField(blank = True, max_length = 150)
	COMPANY = models.CharField(blank = True, max_length = 150,  unique=False)
	RFC = models.CharField(blank = True, max_length = 50, unique=True)
	DATE_1 = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ('NAME',)
		verbose_name = 'Cliente'
		default_permissions = ('add', 'change', 'delete', 'view')
	def __unicode__(self):
		return '%s' % self.NAME

class Contacts_Data(models.Model):
	COMPANY = models.ForeignKey('Clients', on_delete=models.CASCADE)
	POSITION = models.CharField(blank = True, max_length = 50)
	CONTACT_NAME_1 = models.CharField(max_length=50)
	PHONE_1 = models.CharField(max_length=10)
	EXT_1 = models.CharField(max_length=5)
	MAIL_1 = models.EmailField(max_length=50, blank=True)
	PHONE_2 = models.CharField(max_length=10, blank=True)
	EXT_2 = models.CharField(max_length=5, blank=True)
	MAIL_2 = models.EmailField(max_length=50, blank=True)
	def __unicode__(self):
		return '%s - %s (%s)' % (self.CONTACT_NAME_1, self.POSITION, self.COMPANY.NAME)

