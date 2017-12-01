# -*- coding: utf-8
from __future__ import unicode_literals
from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import User


#Pre_delete signal to delete files
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver

GENDER_CHOICES = (
    ('w', 'Mujer'),
    ('m', 'Hombre'),
)

################
# user profile #
################
class Profile(models.Model):
	user = models.OneToOneField(User)
	curp = models.CharField(max_length=20, blank=True)
	rfc = models.CharField(max_length=15, null=True, blank=True)
	social_number = models.CharField(max_length=15, null=True, blank=True)
	birthday = models.DateField(null=True, blank=True)
	address = models.CharField(max_length=200, blank=True)
	phone = models.CharField(max_length=20, blank=True)
	cellphone = models.CharField(max_length=20, blank=True)
	education_degree = models.CharField(max_length=150, blank=True)
	gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='w', verbose_name='Genero')
	blood_type = models.CharField(max_length=50, blank=True)


################
# user contact #
################
class Contact(models.Model):
	user = models.OneToOneField(User)
	first_name = models.CharField(max_length=50, blank=True)
	last_name = models.CharField(max_length= 100, blank=True)
	cellphone = models.CharField(max_length=20, blank=True)
	phone = models.CharField(max_length=20, blank=True)
	email = models.CharField(max_length=100, blank=True)
	observations = models.CharField(max_length=250, blank=True)


###############
# Hiring data #
###############
class Hiring(models.Model):
	#contract = models.ForeignKey(Contracts, blank=True, null=True)
	user = models.OneToOneField(User)
	job_position = models.CharField(max_length=100, blank=True)
	hire_date = models.DateField(null=True, blank=True)
	end_date = models.DateField(null=True, blank=True)
	v_type = models.CharField(max_length=10, blank=True)
	abv = models.CharField(max_length=3, blank=True, verbose_name='Abreviación')
	title = models.CharField(max_length=5, blank=True, verbose_name='Prefijo de Titulo')
	#bank_name = models.CharField(max_length=50, blank=True)
	#clabe = models.CharField(max_length=15, blank=True)
	def __unicode__ (self):
		return self.user



