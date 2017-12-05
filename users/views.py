# -*- coding: utf-8
from __future__ import unicode_literals
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User, Group
from django.core.urlresolvers import reverse
from django.shortcuts import render, render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, RequestContext
from django.template.loader import get_template
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template import Template
from . import forms
from . import models
from django.forms import inlineformset_factory
# Class based views
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView
from digg_paginator import DiggPaginator

##########################
#  Render all the Users  #
##########################
@method_decorator(login_required(login_url='index:login'), name='dispatch')
@method_decorator(permission_required('auth.add_user', login_url='index:view'), name='dispatch')
class view(ListView):
	model = User
	paginator_class = DiggPaginator
	paginate_by = 20
	template_name = 'views/users/users.html'
	def get_queryset(self, *args, **kwargs):
		qs = super(view, self).get_queryset(*args, **kwargs).exclude(is_superuser=1).order_by('username')
		if 'query' in self.request.GET:
			query = self.request.GET['query']
			qs =(qs.filter(last_name__icontains=query)|
				qs.filter(first_name__icontains=query)|
				qs.filter(username__icontains=query)|
				qs.filter(hiring__end_date__icontains=query)).exclude(is_superuser=1)
		return qs
	def get_context_data(self, *args, **kwargs):
		context = super(view, self).get_context_data(*args, **kwargs)
		if 'query' in self.request.GET:
			context["query"] = self.request.GET['query']
			context["subtitle"] = "Resultados de Búsqueda"
			context["btn"] = "Limpiar"
			context["btn_url"] = reverse("users:view")
		else:
			context["subtitle"] = "Lista de Empleados"
			context["btn"] = "Nuevo Usuario"
			context["btn_url"] = reverse("users:new")
		context["results"] = self.get_queryset().count()
		context["title"] = "Empleados"
		context["q_url"] = reverse("users:view")
		return context


#######################################
#  Register a New User in the system  #
#######################################
@permission_required('auth.add_user', login_url='/')
@login_required(login_url='login')
def new(request):
	object_list = Group.objects.all()
	title = "Nuevo Empleado"
	subtitle = "Agregar un usuario nuevo al sistema"
	page = "Formulario de registro"
	btn = "Cancelar"
	btn_url = reverse("users:view")
	if request.method == 'POST':
		form = forms.UserRegisterForm(request.POST or None)
		if form.is_valid():
			user = form.save(commit=False)
			password = form.cleaned_data.get('password')
			user.set_password(password)
			user.save()
			user.groups.add(form.cleaned_data.get('groups'))
			messages.success(request, 'Se ha agregado el usuario %s Correctamente'%(user.username))
			return HttpResponseRedirect(reverse('users:view'))
		else:
			messages.error(request, 'Error al crear Usuario, verifica tu información')
	else:
		form = forms.UserRegisterForm()
	return render(request, 'forms/new_p.html', locals())

###################################
#  Delete User from the database  #
###################################
#   Delete Group data   #
@permission_required('auth.delete_user', login_url='/')
@login_required (login_url='index:login')
def delete(request, pk):
	btn_update = 'Eliminar'
	btn = 'Cancelar'
	btn_url = reverse('users:view')
	object = get_object_or_404(User, id=pk)
	title = object.username
	variable_delete = object.username
	subtitle = 'Eliminar Usuario del Sistema'
	if request.method == 'POST':
		delete = object.delete()
		messages.info(request, 'Usuario %s borrado satisfactoriamente'%(object.get_full_name()))
		return HttpResponseRedirect(reverse('users:view'))
	return render(request, 'forms/delete.html', locals())

##################
#  SUSPEND USER  #
##################
@permission_required('auth.change_user', login_url='/')
@login_required (login_url='login')
def suspend(request, pk):
	btn = 'Cancelar'
	btn_url = reverse('users:view')
	object = get_object_or_404(User.objects.exclude(is_superuser=1), id=pk)
	if object.is_active == True:
		title = 'Suspender Usuario'
		page = 'no podrá hacer uso del sistema pero su información quedará conservada.'
		btn_sus = 'Suspender'
		status = 0
		bg = 'ff902b'
		msg = 'Se ha suspendido el Usuario %s satisfactoriamente'%object.get_full_name()
	else:
		title = 'Habilitar usuario'
		page = 'podrá hacer uso del sistema nuevamente.'
		btn_sus = 'Habilitar'
		status = 1
		bg = '3483e7'
		msg = 'Se ha Habilitado el Usuario %s satisfactoriamente'%object.get_full_name()
	if (request.POST.get('confirm')):
		User.objects.filter(id=pk).update(is_active=status)
		messages.info(request, msg)
		return HttpResponseRedirect(reverse('users:view'))
	return render(request, 'forms/suspend.html', locals())
