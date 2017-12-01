# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth import logout, authenticate, login, get_user_model
from django.contrib.auth.models import User, Group
from . import models
from settings.my_forms import as_myp
from settings.choices import Birthday, BloodChoices, GenderChoices, RelationshipChoices, HireDate, EndDate, AsesorChoices
from settings import validators

################
#   UserForm   #
################
class UserRegisterForm(forms.ModelForm):
	username = forms.CharField(min_length=8, label='@Usuario *', 
		widget=forms.TextInput(attrs={
			'placeholder': 'Nombre de Usuario', 
			'class': 'form-control'}), validators=[validators.user_name])
	email = forms.EmailField(label='Email*', 
		widget=forms.TextInput(attrs={
			'placeholder': 'Dirección de correo electrónico', 
			'class': 'form-control'}))
	first_name = forms.CharField(label='Nombre(s) *', 
		widget=forms.TextInput(attrs={
			'placeholder': 'Nombre(s)', 
			'class': 'form-control'}))
	last_name = forms.CharField(label='Apellido(s) *', 
		widget=forms.TextInput(attrs={
			'placeholder': 'Apellido(s)', 
			'class': 'form-control'}))
	
	class Meta:
		model = User
		fields = ['username', 'email', 'first_name', 'last_name']
	def clean_username(self):
		return self.cleaned_data.get('username').lower()
	def clean_first_name(self):
		return self.cleaned_data.get('first_name').title()
	def clean_last_name(self):
		return self.cleaned_data.get('last_name').title()
	as_myp = as_myp

############################
#   Update Password Form   #
############################
class UserChangePassword(forms.ModelForm):
	password = forms.CharField(min_length=8, label='Contraseña Nueva', widget=forms.PasswordInput(attrs={'placeholder': 'Contraseña', 'class': 'form-control'}))
	password2 = forms.CharField(min_length=8, label='Confirmar Contraseña', widget=forms.PasswordInput(attrs={'placeholder': 'Confirmar Contraseña', 'class': 'form-control'}))
	class Meta:
		model = User
		fields = ['password', 'password2']
	def clean_password2(self):
		password2 = self.cleaned_data.get('password2')
		password = self.cleaned_data.get('password')
		if password2 != password:
			raise forms.ValidationError('Las contraseñas no coinciden')
	as_myp = as_myp



####################
#   Profile form   #
####################
class ProfileForm(forms.ModelForm):
	curp = forms.CharField(required=False, label='C.U.R.P.', widget=forms.TextInput(attrs={'placeholder':'', 'class':'form-control'}))
	rfc = forms.CharField(required=False, label='R.F.C.', widget=forms.TextInput(attrs={'placeholder':'', 'class':'form-control'}))
	social_number = forms.CharField(required=False, label='Número de Seguro Social', widget=forms.TextInput(attrs={'placeholder':'', 'class':'form-control'}))
	birthday = forms.DateField(label='Fecha de Cumpleaños', widget=forms.TextInput(attrs=Birthday))
	address = forms.CharField(required=False, label='Dirección', widget=forms.TextInput(attrs={'placeholder':'', 'class':'form-control'}))
	phone = forms.CharField(required=False, label='Teléfono de Casa', widget=forms.TextInput(attrs={'placeholder':'', 'class':'form-control'}))
	cellphone = forms.CharField(required=False, label='Número Celular', widget=forms.TextInput(attrs={'placeholder':'', 'class':'form-control'}))
	education_degree = forms.CharField(required=False, label='Escolaridad', widget=forms.TextInput(attrs={'placeholder':'', 'class':'form-control'}))
	blood_type = forms.CharField(required=False, label='Grupo Sanguíneo', widget=forms.Select(choices=BloodChoices, attrs={'class': 'form-control'}))	
	#gender = forms.CharField(required=False, label='Genero', widget=forms.Select(choices=GenderChoices, attrs={'class': 'form-control'}))
	def clean_rfc(self):
		return self.cleaned_data.get('rfc').upper()
	def clean_curp(self):
		return self.cleaned_data.get('curp').upper()
	class Meta:
		model = models.Profile
		exclude = ('user',)
	as_myp = as_myp




####################
#   Contact Form   #
####################
class ContactForm(forms.ModelForm):
	first_name = forms.CharField(required=False, label='Nombre(s)', widget=forms.TextInput(attrs={'placeholder':'', 'class':'form-control'}))
	last_name = forms.CharField(required=False, label='Apellido(s)', widget=forms.TextInput(attrs={'placeholder':'', 'class':'form-control'}))
	cellphone = forms.CharField(required=False, label='Teléfono Celular', widget=forms.TextInput(attrs={'placeholder':'', 'class':'form-control'}))
	phone = forms.CharField(required=False, label='Teléfono Particular', widget=forms.TextInput(attrs={'placeholder':'', 'class':'form-control'}))
	email = forms.EmailField(required=False, label='Email', widget=forms.TextInput(attrs={'placeholder':'', 'class':'form-control'}))
	observations = forms.CharField(required=False, label='Parentesco', widget=forms.Select(choices=RelationshipChoices, attrs={'class': 'form-control'}))
	def clean_first_name(self):
		return self.cleaned_data.get('first_name').title()
	def clean_last_name(self):
		return self.cleaned_data.get('last_name').title()
	class Meta:
		model = models.Contact
		#cc
		exclude = ('user',)
	as_myp = as_myp

####################
#   Hiring Form   #
####################
class HiringForm(forms.ModelForm):
	#contract = forms.ModelChoiceField(required=False, label='Tipo de Contrato', queryset=models.Contracts.objects.all(), widget=forms.Select(attrs={ 'class':  'form-control'}))
	job_position = forms.CharField(required=True, label='Puesto', widget=forms.TextInput(attrs={'placeholder':'', 'class':'form-control'}))
	hire_date = forms.DateField(required=False, label='Fecha de Contratación', widget=forms.TextInput(attrs=HireDate))
	end_date = forms.DateField(required=False, label='Fecha de Término', widget=forms.TextInput(attrs=EndDate))
	abv = forms.CharField(required=False, label='Abreviación', widget=forms.TextInput(attrs={'placeholder':'', 'class':'form-control'}))
	title = forms.CharField(required=False, label='Título', widget=forms.TextInput(attrs={'placeholder':'Ing.', 'class':'form-control'}))
	#bank_name = forms.CharField(required=False, label='Nombre de Banco', widget=forms.TextInput(attrs={'placeholder':'', 'class':'form-control'}))
	#clabe = forms.CharField(required=False, label='Número CLABE', widget=forms.TextInput(attrs={'placeholder':'', 'class':'form-control'}))
	def clean_job_position(self):
		return self.cleaned_data.get('job_position').title()
	class Meta:
		model = models.Hiring
		exclude = ('user', 'v_type')
	as_myp = as_myp


class GroupForm(forms.ModelForm):
	groups = forms.ModelChoiceField(required=True, label='Asignar Grupo',
		queryset=Group.objects.all(), 
		widget=forms.Select(attrs={ 'class':  'form-control'}))
	class Meta:
		model = User
		fields = ['groups',]
	as_myp = as_myp