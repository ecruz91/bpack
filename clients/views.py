# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from django.contrib import messages
from django.shortcuts import render, render_to_response, get_object_or_404
from django.core.urlresolvers import reverse
from . import models
from . import forms
from django.http import HttpResponseRedirect, HttpResponse
from django.forms.formsets import formset_factory
import datetime
from django.contrib.auth.models import User

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, permission_required
# Class based views
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from digg_paginator import DiggPaginator
from django.http import JsonResponse
#from registers.forms import querydate
#from registers.models import Registers
from datetime import datetime, timedelta
#Render all the clients in the system
@method_decorator(login_required(login_url='login'), name='dispatch')
@method_decorator(permission_required('clients.add_clients', login_url='home'), name='dispatch')
class list_clients(ListView):
	model = models.Clients
	paginate_by = 12
	paginator_class = DiggPaginator
	template_name = 'views/clients/clients.html'
	def get_queryset(self, *args, **kwargs):
		qs = super(list_clients, self).get_queryset(*args, **kwargs).order_by('-id')
		if 'query' in self.request.GET:
			query = self.request.GET['query']
			qs =(qs.filter(COMPANY__icontains=query)|
				qs.filter(NAME__icontains=query)|
				qs.filter(CID__iexact=query)|
				qs.filter(RFC__icontains=query)|
				qs.filter(contacts_data__CONTACT_NAME_1__contains=query)|
				qs.filter(contacts_data__MAIL_1__contains=query)|
				qs.filter(contacts_data__PHONE_1__contains=query)|
				qs.filter(contacts_data__MAIL_2__contains=query)|
				qs.filter(contacts_data__PHONE_2__contains=query)).reverse()[:100]
		return qs
	def get_context_data(self, *args, **kwargs):
		context = super(list_clients, self).get_context_data(*args, **kwargs)
		if 'query' in self.request.GET:
			context["query"] = self.request.GET['query']
			context["subtitle"] = "Resultados de Búsqueda"
			context["btn"] = "Limpiar"
			context["btn_url"] = reverse("clients:view")
		else:
			context["subtitle"] = "Clientes en el Sistema"
			context["btn"] = "Registrar Cliente"
			context["btn_url"] = reverse("clients:new")
		context["results"] = self.get_queryset().count()
		context["title"] = "Clientes"
		context["q_url"] = reverse("clients:view")
		return context



# Register a New Client in the system #
@login_required (login_url='login')
@permission_required('clients.add_clients', login_url='index:login')
def new_clients(request):
	title = "Agregar Nuevo Cliente"
	subtitle = 'Registrar cliente en el sistema'
	btn = 'Cancelar'
	btn_url = reverse('clients:view')
	form = forms.new_client(request.POST or None)
	if request.method == 'POST':
		if form.is_valid():
			f = form.save(commit=False)
			f.save()
			messages.success(request, 'Se Agregó el cliente al sistema')
			return HttpResponseRedirect(reverse("clients:view"))
		else:
			messages.error(request, 'Error al crear cliente, Revisa tu información')
	return render(request, 'forms/new_p.html', locals())

#  Edit a Client in the system  #
@login_required (login_url='login')
@permission_required('clients.change_clients', login_url='index:login')
def edit_client(request, pk):
	btn = 'Ver Cliente'
	btn_url = reverse('clients:profile', kwargs={'pk':pk})
	object = get_object_or_404(models.Clients.objects, id=pk)
	client = object.NAME
	title = 'Editar {0}'.format(client)
	subtitle = 'Editar información del Cliente'
	form = forms.new_client(request.POST or None, instance=object)
	if request.method == 'POST':
		if form.is_valid():
			update = form.save(commit=False)
			update.save()
			messages.success(request, 'Se Actualizó el Cliente Satisfactoriamente')
			return HttpResponseRedirect(reverse('clients:profile', kwargs={'pk':pk}))
		else:
			messages.error(request, 'Revisa tu información')
	return render(request, 'forms/new_p.html', locals())

#  Edit the Main Contact #
@login_required (login_url='login')
def contact(request, pk):
	btn = 'Cancelar'
	btn_url = reverse('clients:profile', kwargs={'pk':pk})
	object = get_object_or_404(models.Clients.objects, id=pk)
	client = object.NAME
	title = '{0}'.format(client)
	subtitle = 'Editar Contacto Principal'
	form = forms.contact(request.POST or None, instance=object)
	if request.method == 'POST':
		if form.is_valid():
			update = form.save(commit=False)
			update.save()
			messages.success(request, 'Se Actualizó la información del Cliente')
			return HttpResponseRedirect(reverse('clients:profile', kwargs={'pk':pk}))
		else:
			messages.error(request, 'Revisa tu información')
	return render(request, 'forms/new_p.html', locals())

#  New Contact #
@login_required (login_url='login')
def new_contact(request, pk):
	btn = 'Cancelar'
	btn_url = reverse('clients:profile', kwargs={'pk':pk})
	object = get_object_or_404(models.Clients.objects, id=pk)
	if models.Contacts_Data.objects.filter(COMPANY__id=pk).count() >= 7:
		messages.info(request, 'Sólo se pueden añadir 7 Contactos')
		return HttpResponseRedirect(reverse('clients:profile', kwargs={'pk':pk}))
	client = object.NAME
	title = 'Nuevo Contacto para {0}'.format(client)
	subtitle = 'Agregar Contacto a Cliente'
	form = forms.contacts(request.POST or None)
	if request.method == 'POST':
		if form.is_valid():
			f = form.save(commit=False)
			f.COMPANY = object
			f = form.save()
			messages.success(request, 'Se Actualizó la información del Cliente')
			return HttpResponseRedirect(reverse('clients:profile', kwargs={'pk':pk}))
		else:
			messages.error(request, 'Revisa tu información')
	return render(request, 'forms/new_p.html', locals())

#Edit the Main Contact #
@login_required (login_url='login')
def contacts(request, pk):
	btn = 'Cancelar'
	object = get_object_or_404(models.Contacts_Data.objects, id=pk)
	title = 'Editar Contacto'
	subtitle = 'Editar Contacto del Cliente'
	pk_1 = object.COMPANY_id
	btn_url = reverse('clients:profile', kwargs={'pk':pk_1})
	form = forms.contacts(request.POST or None, instance=object)
	if request.method == 'POST':
		if form.is_valid():
			f = form.save(commit=False)
			f = form.save()
			messages.success(request, 'Se Actualizó el Contacto satisfactoriamente')
			return HttpResponseRedirect(reverse('clients:profile', kwargs={'pk':pk_1}))
		else:
			messages.error(request, 'Revisa tu información')
	return render(request, 'forms/new_p.html', locals())

@login_required (login_url='login')
def delete_contacts(request, pk):
	btn = 'Cancelar'
	object = get_object_or_404(models.Contacts_Data.objects, id=pk)
	title = 'Eliminar Información de {0}'.format(object.CONTACT_NAME_1,)
	variable_delete = object.CONTACT_NAME_1
	subtitle = 'Eliminar Contacto del Cliente'
	pk_1 = object.COMPANY_id
	btn_url = reverse('clients:profile', kwargs={'pk':pk_1})
	if request.method == 'POST':
		messages.info(request, 'Se eliminó el contacto satisfactoriamente')
		delete = object.delete()
		return HttpResponseRedirect(reverse('clients:profile', kwargs={'pk':pk_1}))
	return render(request, "forms/delete.html", locals())



#  Delete Client from the database  #
@method_decorator(login_required(login_url='login'), name='dispatch')
@method_decorator(permission_required('clients.delete_clients', login_url='/'), name='dispatch')
class delete_client(DeleteView):
	template_name = "forms/delete.html"
	model = models.Clients
	def delete(self, request, *args, **kwargs):
		success_message = 'Se eliminó el Cliente seleccionado'
		messages.info(self.request, success_message)
		return super(delete_client, self).delete(request, *args, **kwargs)
	def get_success_url(self):
		return reverse("clients:view")
	def get_context_data(self, *args, **kwargs):
		context = super(delete_client, self).get_context_data(*args, **kwargs)
		object = get_object_or_404(models.Clients.objects, id=self.kwargs['pk'])
		object_delete = object.NAME
		context["variable_delete"] = object_delete
		context["title"] = "Eliminar cliente del sistema"
		context["subtitle"] = "Estás a punto de eliminar a este cliente"
		context["btn"] = "Cancelar"
		context["btn_url"] = reverse("clients:view")
		context["page"] = "¿Estás seguro?"
		return context

@login_required (login_url='login')
def profile_clients(request, pk):
	object = get_object_or_404(models.Clients.objects, id=pk)
	btn = 'Cancelar'
	contacts = models.Contacts_Data.objects.filter(COMPANY__id=pk)
	btn_url = reverse('clients:view')
	title = object.NAME
	subtitle = 'Datos de Cliente'
	return render(request, 'views/clients/client.html', locals())
