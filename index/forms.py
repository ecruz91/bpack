# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django import forms
from django.contrib.auth import logout, authenticate, login, get_user_model
#from django.core.validators import RegexValidator
#from settings.validators import password_strength
User = get_user_model()

class Login_Form(forms.Form):
	username = forms.CharField(min_length=8,
		widget=forms.TextInput(
			attrs={
			'placeholder':'Correo Electrónico'
			}))
	password = forms.CharField(min_length=8,
		widget=forms.PasswordInput(
			attrs={
			'placeholder':'Contraseña'
			}))
	def clean(self, *args, **kwargs):
		username = self.cleaned_data.get("username").lower()
		password = self.cleaned_data.get("password")
		if username and password:
			user = authenticate(username=username, password=password)
			if not user:
				raise forms.ValidationError("Este usuario no existe")
		return super(Login_Form, self).clean(*args,**kwargs)
	def __init__(self, *args, **kwargs):
		super(Login_Form, self).__init__(*args, **kwargs)
		for field_name, field in self.fields.items():
			field.widget.attrs['class'] = 'form-control'

class Check_Password_Form(forms.Form):
	password = forms.CharField(
		widget=forms.PasswordInput(
			attrs={
			'placeholder':'Contraseña'
			}))

	def __init__(self, *args, **kwargs):
		super(Check_Password_Form, self).__init__(*args, **kwargs)
		for field_name, field in self.fields.items():
			field.widget.attrs['class'] = 'form-control'

