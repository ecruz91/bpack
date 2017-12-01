# -*- coding: utf-8
from django import forms
from easy_select2 import Select2Multiple
from . import models
from settings import validators
from settings.choices import STATE_CHOICES, CITY_CHOICES, SOURCE_CHOICES, TYPE_CHOICES, COUNTRY_CHOICES, job_tittle
import datetime
from settings.my_forms import as_myp
from django.forms import ModelForm
from django.contrib.auth.models import User


now = datetime.datetime.now()
today = now.strftime("%Y-%m-%d %H:%M")



class new_client(ModelForm):
	CID = forms.CharField(required=True, 
		min_length=5,
		max_length=8,
		label='ID de Cliente*:', 
		widget=forms.TextInput(attrs={'placeholder': 'B000292', 
			'class':  'form-control'}), 
		validators=[validators.lenght_min, validators.lenght_max])
	COMPANY = forms.CharField(required=True, 
		label='Razón Social*:', 
		widget=forms.TextInput(attrs={'placeholder': 'ACME SA de CV', 
			'class':  'form-control'}), 
		validators=[validators.lenght_min, validators.lenght_max])
	
	NAME = forms.CharField(required=True, 
		label='Cliente *:', 
		widget=forms.TextInput(attrs={'placeholder': 'ACME', 
			'class': 'form-control'}), 
		validators=[validators.lenght_min, validators.lenght_max])
	
	RFC = forms.CharField(required=True, 
		label='RFC *', 
		widget=forms.TextInput(attrs={'placeholder': 'Ejemplo: ABC680524P76', 
			'class': 'form-control'}), 
		validators=[validators.rfc])
	
	
	DATE_1 = forms.CharField(required=False, 
		widget=forms.HiddenInput(), 
		initial=today)

	

	class Meta:
		model = models.Clients
		fields = '__all__'
		#exclude = ('CID',)
	def clean_CID(self):
		return self.cleaned_data.get('CID').upper()
	def clean_RFC(self):
		return self.cleaned_data.get('RFC').upper()
	def clean_COMPANY(self):
		return self.cleaned_data.get('COMPANY').upper()
	def clean_NAME(self):
		return self.cleaned_data.get('NAME').upper()
	as_myp = as_myp


class contact(ModelForm):
	CONTACT_NAME_1 = forms.CharField(
		required=False, 
		label='Persona de Contacto*:',
		widget=forms.TextInput(attrs={
			'placeholder': 'Nombre',
			'class':'form-control'}), 
		validators=[validators.lenght_min, validators.lenght_max])

	POSITION =  forms.CharField(required=False, 
		label='Puesto*:', 
		widget=forms.TextInput(attrs={'placeholder': 'Puesto', 
			'class': 'form-control'}))
	
	PHONE_1 = forms.CharField(
		required=False, 
		label='Teléfono*:', 
		widget=forms.TextInput(
			attrs={
			'placeholder': '4425555555', 
			'class': 'form-control'}), 
		validators=[validators.phone])
	
	EXT_1 = forms.CharField(
		required=False, 
		label='Ext', 
		widget=forms.TextInput(
			attrs={
		'placeholder': 'EXT', 
		'class': 'form-control'}), 
		validators=[validators.ext])
	
	MAIL_1 = forms.EmailField(
		required=False, 
		label='Correo Electrónico', 
		widget=forms.EmailInput(
			attrs={
		'placeholder': 'contacto@mail.com', 
		'class': 'form-control'}))	
	
	PHONE_2 = forms.CharField(
		required=False, 
		label='Teléfono Adicional',
		widget=forms.TextInput(
			attrs={
		'placeholder': '4425555555', 
		'class': 'form-control'}), 
		validators=[validators.phone])
	
	EXT_2 = forms.CharField(
		required=False, 
		 widget=forms.TextInput(
		 	attrs={
		 'placeholder': 'EXT', 
		 'class': 'form-control'}), 
		 validators=[validators.ext])
	
	MAIL_2 = forms.EmailField(
		required=False, 
		label='Correo Adicional', 
		widget=forms.EmailInput(attrs={
			'placeholder': 'contacto2@mail.com', 
			'class': 'form-control'}))

	class Meta:
		model = models.Clients
		fields = ('CONTACT_NAME_1', 'POSITION', 'PHONE_1', 'EXT_1', 'PHONE_2', 'EXT_2', 'MAIL_1', 'MAIL_2',)
		#exclude = ('VENDOR',)

	def clean_CONTACT_NAME_1(self):
		return self.cleaned_data.get('CONTACT_NAME_1').title()
	as_myp = as_myp

class contacts(ModelForm):
	CONTACT_NAME_1 = forms.CharField(required=True, label='Persona de Contacto*:', widget=forms.TextInput(attrs={'placeholder': 'Nombre', 'class':  'form-control'}), validators=[validators.lenght_min, validators.lenght_max])
	POSITION = forms.CharField(required=True, label='Puesto:', widget=forms.TextInput(attrs={'class': 'form-control'}))
	PHONE_1 = forms.CharField(required=True, label='Teléfono*:', widget=forms.TextInput(attrs={'placeholder': '4425555555', 'class': 'form-control'}), validators=[validators.phone])
	EXT_1 = forms.CharField(required=False, label='Ext', widget=forms.TextInput(attrs={'placeholder': 'EXT', 'class': 'form-control'}), validators=[validators.ext])
	MAIL_1 = forms.EmailField(required=True, label='Correo Electrónico', widget=forms.EmailInput(attrs={'placeholder': 'contacto@mail.com', 'class': 'form-control'}))	
	PHONE_2 = forms.CharField(required=False, label='Teléfono Adicional', widget=forms.TextInput(attrs={'placeholder': '4425555555', 'class': 'form-control'}), validators=[validators.phone])
	EXT_2 = forms.CharField(required=False,  widget=forms.TextInput(attrs={'placeholder': 'EXT', 'class': 'form-control'}), validators=[validators.ext])
	MAIL_2 = forms.EmailField(required=False, label='Correo Adicional', widget=forms.EmailInput(attrs={'placeholder': 'contacto2@mail.com', 'class': 'form-control'}))

	class Meta:
		model = models.Contacts_Data
		fields = ('CONTACT_NAME_1', 'POSITION', 'PHONE_1', 'EXT_1', 'PHONE_2', 'EXT_2', 'MAIL_1', 'MAIL_2',)
		#exclude = ('VENDOR',)

	def clean_CONTACT_NAME_1(self):
		return self.cleaned_data.get('CONTACT_NAME_1').title()
	as_myp = as_myp
