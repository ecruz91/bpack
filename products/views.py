# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import logout, authenticate, login
from django.shortcuts import render
from . import models, forms
from clients.forms import new_client
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.template.loader import get_template
from django.template import Context, RequestContext
from django.contrib import messages
import json
from django.utils.safestring import mark_safe
# Create your views here.
# Class based views
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView

from django.http import HttpResponse, Http404, HttpResponseRedirect
from digg_paginator import DiggPaginator
@method_decorator(permission_required('products.view_product', login_url='index:login'), name='dispatch')
@method_decorator(login_required(login_url='index:login'), name='dispatch')
class view(ListView):
	model = models.Product
	paginator_class = DiggPaginator
	paginate_by = 30
	template_name = 'views/products/products.html'
	def get_queryset(self, *args, **kwargs):
		qs = super(view, self).get_queryset(*args, **kwargs).order_by('-updated')
		if 'query' in self.request.GET:
			query = self.request.GET['query']
			qs = (qs.filter(pid__icontains=query)|
				qs.filter(producto__icontains=query)|
				qs.filter(descripcion__icontains=query))
		return qs
	def get_context_data(self, *args, **kwargs):
		context = super(view, self).get_context_data(*args, **kwargs)
		context["results"] = self.get_queryset().count()
		context["q_url"] = reverse("products:view")
		if 'query' in self.request.GET:
			context["query"] = self.request.GET['query']
			context["btn"] = "Limpiar"
			context["btn_url"] = reverse("products:view")
			context["subtitle"] = "Resultados de Búsqueda"
		else:
			context["subtitle"] = "Productos en el Sistema"
			context["btn"] = "Nuevo Producto"
			context["btn_url"] = reverse("products:new")

		context["title"] = "Productos"
		return context


@permission_required('products.add_product', login_url='index:login')
@login_required (login_url='index:login')
def new(request):
	btn_update = 'Guardar'
	btn = 'Cancelar'
	btn_url = reverse('products:view')
	title = 'Dar de alta Producto'
	subtitle = 'Formulario de Alta de Productos'
	if request.method == 'POST':
		form = forms.ProductForm(request.POST, request.FILES)
		form2 = new_client(request.POST or None)
		if form.is_valid():
			form.save()
			messages.success(request, 'Producto creado correctamente')
			return HttpResponseRedirect(reverse('products:view'))
		else:
			messages.error(request, 'Error al Crear el Producto')
	else:
		form2 = new_client()
		form = forms.ProductForm()
	return render(request, 'forms/new_product.html', locals())

@permission_required('products.change_product', login_url='index:login')
@login_required (login_url='index:login')
def edit(request, pk):

	btn_update = 'Actualizar Producto'
	btn = 'Cancelar'
	btn_url = reverse('products:view')
	object = get_object_or_404(models.Product, id=pk)
	title = 'Editar {0}'.format(object,)
	subtitle = 'Editar Productos'
	if request.method == 'POST':
		form = forms.ProductForm(request.POST or None, instance=object)
		form2 = new_client(request.POST or None)
		if form.is_valid():
			update = form.save(commit=True)
			update.save()
			messages.success(request, 'Se actualizó el producto %s'%(object))
			return HttpResponseRedirect(reverse('products:view'))
		else:
			messages.error(request, 'Verifica tu información')
	else:
		form2 = new_client()
		form = forms.ProductForm(instance=object)
	return render(request, 'forms/new_product.html', locals())

@permission_required('products.delete_product', login_url='index:login')
@login_required (login_url='index:login')
def delete(request, pk):
	btn = 'Cancelar'
	object = get_object_or_404(models.Product.objects, id=pk)

	#variable_delete = object.CONTACT_NAME_1
	subtitle = 'Eliminar Contacto del Cliente'
	btn_url = reverse('products:view')
	if request.method == 'POST':
		messages.info(request, 'Se eliminó el Producto %s satisfactoriamente'%(object))
		delete = object.delete()
		return HttpResponseRedirect(reverse('products:view'))
	return render(request, "forms/delete.html", locals())





def ajax_response(request):
	success = None
	errors_dict = None
	if request.method == 'POST':
		form = new_client(request.POST or None)
		form.CID = request.POST.get('CID','')
		form.COMPANY = request.POST.get('COMPANY','')
		form.NAME = request.POST.get('NAME','')
		form.RFC = request.POST.get('RFC','')
		if form.is_valid():
			success = True
			form.save()
			messages.success(request, 'Cliente creado correctamente')
		else:
			success = False
			errors_dict = []
			for data in form.errors:
				result = {"label":form[data].label, "error":form[data].errors}
				errors_dict.append(result)
		to_json = {'success':success}
		return HttpResponse(json.dumps({'to_json':to_json,'errors_dict':errors_dict}, indent=3), content_type="application/json")

	else:
		raise Http404
