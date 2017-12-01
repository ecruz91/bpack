# -*- coding: utf-8 -*-

from django import forms
from django.contrib.auth import logout, authenticate, login, get_user_model
from django.core.validators import RegexValidator
from models import Orders, Pallets
from settings.my_forms import as_myp
from django.template.defaultfilters import mark_safe

User = get_user_model()

class OrderForm(forms.ModelForm):
	packer = forms.ModelChoiceField(required=True,
	label = mark_safe('<label id="packer_id_label">Empacador</label>'),
	queryset=User.objects.filter(groups__name__in=['empacador']),
	widget=forms.Select(attrs={}))
	def __init__(self, *args, **kwargs):
		super(OrderForm, self).__init__(*args,**kwargs)
		for field_name, field in self.fields.items():
			field.widget.attrs['class'] = 'form-control'


	class Meta:
		model = Orders
		exclude = ('flag', 'packer_name', 'client_name', 'product_name')


	def clean_bpid(self):
		return self.cleaned_data.get('bpid').upper()
	def clean_order(self):
		return self.cleaned_data.get('order').upper()


	as_myp = as_myp


class Order_Pallet(forms.ModelForm):
	name = forms.CharField(required=True,
		label='tarima',
		widget=forms.TextInput(attrs={'placeholder': 'Tarima',
				'class':'form-control'}))
	class Meta:
		model = Pallets
		fields = '__all__'


	as_myp = as_myp
