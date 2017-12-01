# -*- coding: utf-8
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

# View Groups #
@method_decorator(login_required(login_url='index:login'), name='dispatch')
class view(ListView):
    paginator_class = DiggPaginator
    model = Group
    paginate_by = 20
    template_name = 'views/groups/groups.html'
    def get_queryset(self, *args, **kwargs):
        qs = super(view, self).get_queryset(*args, **kwargs)
        if 'query' in self.request.GET:
            query = self.request.GET['query']
            qs =(qs.filter(name__icontains=query))
        return qs
    def get_context_data(self, *args, **kwargs):
        context = super(view, self).get_context_data(*args, **kwargs)
        if 'query' in self.request.GET:
            context["query"] = self.request.GET['query']
            context["subtitle"] = "Resultados de Búsqueda"
            context["btn"] = "Limpiar"
            context["btn_url"] = reverse("groups:view")
        else:
            context["subtitle"] = "Lista de Grupos"
            context["btn"] = "Nuevo Grupo"
            context["btn_url"] = reverse("groups:new")
        context["results"] = self.get_queryset().count()
        context["title"] = "Grupos en el sistema"
        context["q_url"] = reverse("groups:view")
        return context

# Create a New Group  #
@login_required(login_url='index:login')
def new(request):
    if not request.user.is_superuser:
        raise Http404
    title = "Nuevo Grupo"
    subtitle = "Agregar un Grupo al sistema"
    btn = "Cancelar"
    btn_url = reverse("groups:view")
    if request.method == 'POST':
        form = forms.GroupForm(request.POST or None)
        if form.is_valid():
            f = form.save()
            name = f.name
            messages.success(request, 'Se ha creado el Grupo %s Satisfactoriamente.'%(name))
            return HttpResponseRedirect(reverse("groups:view"))
        else:
            messages.error(request, 'No se pudo guardar el Grupo')
    else:
        form = forms.GroupForm()
    return render(request, 'forms/new.html', locals())

#  Edit Group   #
@login_required (login_url='index:login')
def edit(request, pk):
    if not request.user.is_superuser:
        raise Http404
    btn_update = 'Actualizar Grupo'
    btn = 'Cancelar'
    btn_url = reverse('groups:view')
    object = get_object_or_404(Group, id=pk)
    title = object.name
    subtitle = 'Editar Grupo'
    if request.method == 'POST':
        form = forms.GroupForm(request.POST or None, instance=object)
        if form.is_valid():
            update = form.save(commit=True)
            update.save()
            name = update.name
            messages.success(request, 'Se ha actualizado el grupo %s satisfactoriamente.'%(name))
            return HttpResponseRedirect(reverse('groups:view'))
        else:
            messages.error(request, 'No se pudo Actualizar el Grupo')
    else:
        form = forms.GroupForm(instance=object)
    return render(request, 'forms/new.html', locals())

#   Delete Group data   #
@login_required (login_url='index:login')
def delete(request, pk):
    if not request.user.is_superuser:
        raise Http404
    btn_update = 'Eliminar'
    btn = 'Cancelar'
    btn_url = reverse('groups:view')
    object = get_object_or_404(Group, id=pk)
    title = object.name
    variable_delete = object.name
    subtitle = 'Eliminar Grupo de Usuarios'
    if request.method == 'POST':
        delete = object.delete()
        messages.error(request, 'Grupo %s borrado satisfactoriamente'%(object.name))
        return HttpResponseRedirect(reverse('groups:view'))
    return render(request, 'forms/delete.html', locals())
