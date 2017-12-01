# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth import logout, authenticate, login, get_user_model
from django.core.validators import RegexValidator
from django.contrib.auth.models import User, Group, Permission
from settings.my_forms import as_myp, as_myp2
from settings import validators
#User = get_user_model()

class UserRegisterForm(forms.ModelForm):
	username = forms.CharField(min_length=8, label='@Usuario *', 
		widget=forms.TextInput(attrs={'placeholder': 'Nombre de Usuario', 
			'class': 'form-control'}), 
		validators=[validators.user_name])
	email = forms.EmailField(label='Email *', 
		widget=forms.TextInput(attrs={'placeholder': 
			'Dirección de correo electrónico',
			'class': 'form-control'}))
	first_name = forms.CharField(label='Nombre(s) *', 
		widget=forms.TextInput(attrs={'placeholder': 'Nombre(s)', 
			'class': 'form-control'}))
	last_name = forms.CharField(label='Apellido(s) *', 
		widget=forms.TextInput(attrs={'placeholder': 'Apellido(s)', 
			'class': 'form-control'}))
	password = forms.CharField(min_length=8, widget=forms.PasswordInput(attrs={'placeholder': 'Contraseña', 
		'class': 'form-control'}), label='Contraseña *')
	password2 = forms.CharField(min_length=8, widget=forms.PasswordInput(attrs={'placeholder': 'Confirmar Contraseña', 
		'class': 'form-control'}), label='Confirmar Contraseña *')
	groups = forms.ModelChoiceField(required=True, label='Asignar Grupo',
		queryset=Group.objects.all(), 
		widget=forms.Select(attrs={ 'class':  'form-control'}))
	class Meta:
		model = User
		#fields = '__all__'
		fields = ['username', 'email', 'first_name', 'last_name', 'password', 'password2', 'groups']
	def clean_username(self):
		return self.cleaned_data.get('username').lower()
	def clean_first_name(self):
		return self.cleaned_data.get('first_name').title()
	def clean_last_name(self):
		return self.cleaned_data.get('last_name').title()
	def clean_password2(self):
		password2 =self.cleaned_data.get('password2')
		password = self.cleaned_data.get('password')
		if password2 != password:
			raise forms.ValidationError('Las contraseñas no coinciden')
	as_myp = as_myp

class UserChangePassword(forms.ModelForm):
	password = forms.CharField(label='Contraseña Nueva', 
		widget=forms.PasswordInput(attrs={'placeholder': 'Contraseña', 
			'class': 'form-control'}))
	password2 = forms.CharField(label='Confirmar Contraseña',
		widget=forms.PasswordInput(attrs={'placeholder': 'Confirmar Contraseña', 
	 	'class': 'form-control'}))
	class Meta:
		model = User
		fields = ['password', 'password2']
	def clean_password2(self):
		password2 = self.cleaned_data.get('password2')
		password = self.cleaned_data.get('password')
		if password2 != password:
			raise forms.ValidationError('Las contraseñas no coinciden')

class GroupForm(forms.ModelForm):
	class Meta:
		model = Group
		fields = '__all__'
	def __init__(self, *args, **kwargs):
		super(GroupForm, self).__init__(*args, **kwargs)
		self.fields['permissions'].widget.attrs['class'] = 'form-control'
		self.fields['permissions'].widget.attrs['style'] = 'min-height:300px'
		self.fields['name'].widget.attrs['class'] = 'form-control'

