# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth import logout, authenticate, login, get_user_model
from django.core.validators import RegexValidator
from . import models
from clients.models import Clients
from easy_select2 import Select2Multiple
from settings.my_forms import as_myp
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe
from django.forms import widgets
from django.conf import settings
#User = get_user_model()


class RelatedFieldWidgetCanAdd(widgets.Select):

    def __init__(self, related_model, related_url=None, *args, **kw):

        super(RelatedFieldWidgetCanAdd, self).__init__(*args, **kw)

        if not related_url:
            rel_to = related_model
            info = (rel_to._meta.app_label, rel_to._meta.object_name.lower())
            related_url = 'admin:%s_%s_add' % info

        # aqui no jala el reverse :)
        self.related_url = related_url

    def render(self, name, value, *args, **kwargs):
		output = [super(RelatedFieldWidgetCanAdd, self).render(name, value, *args, **kwargs)]
		output.append(u'<br style="line-height:30px;"><button type="button" class="btn btn-default fa fa-plus" data-toggle="modal" data-target="#myModal"> Cliente</button>'
		)
		return mark_safe(u''.join(output))

class ProductForm(forms.ModelForm):
	hidden = forms.ModelChoiceField(required=False, label='', queryset=Clients.objects.all(), widget=RelatedFieldWidgetCanAdd(Clients, related_url="clients:new"))
	def __init__(self, *args, **kwargs):
		super(ProductForm, self).__init__(*args,**kwargs)
		for field_name, field in self.fields.items():
			field.widget.attrs['class'] = 'form-control'


	class Meta:
		model = models.Product
		fields = '__all__'


	def clean_pid(self):
		return self.cleaned_data.get('pid').upper()
	def clean_product(self):
		return self.cleaned_data.get('product').upper()
	def clean_descripcion(self):
		return self.cleaned_data.get('descripcion').upper()

	as_myp = as_myp
