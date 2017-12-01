# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth import logout, authenticate, login, get_user_model
from django.core.validators import RegexValidator
from django.contrib.auth.models import User, Group, Permission
from settings.my_forms import as_myp, as_myp2
from settings import validators
#User = get_user_model()

class GroupForm(forms.ModelForm):
	class Meta:
		model = Group
		fields = '__all__'
	def __init__(self, *args, **kwargs):
		super(GroupForm, self).__init__(*args, **kwargs)
		self.fields['permissions'].widget.attrs['class'] = 'form-control'
		self.fields['permissions'].widget.attrs['style'] = 'min-height:300px'
		self.fields['name'].widget.attrs['class'] = 'form-control'

