# -*- coding: utf-8 -*-
from __future__ import unicode_literals
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
from django.contrib import messages
from . import forms
from . import models
from datetime import datetime, timedelta
# Class based views
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView
from digg_paginator import DiggPaginator
from django.http import HttpResponse, HttpResponseRedirect, Http404
#  User Profile   #
#@permission_required('auth.change_user', login_url='users')
@login_required (login_url='login')
def view(request, pk):
    object = get_object_or_404(User.objects.exclude(is_superuser=1), id=pk)
    if request.user.groups.filter(name='empacador').exists() and request.user.id != object.id:
        raise Http404
    title = object.username
    now = datetime.now().date()
    subtitle = 'Perfil de usuario'
    if request.user.groups.filter(name='administrador').exists() or request.user.is_superuser:
        btn = 'Editar empleado'
        btn_url = reverse('profile:edit', kwargs={'pk':pk})
    return render(request, 'views/profile/profile.html', locals())

#  Edit Profile   #
@permission_required('auth.change_user', login_url='index:view')
@login_required (login_url='login')
def edit(request, pk):
    user_data = 'active'
    btn_update = 'Actualizar Credenciales'
    btn = 'Cancelar'
    btn_url = reverse('users:view')
    object = get_object_or_404(User.objects.exclude(is_superuser=1), id=pk)
    u = object.username
    title = 'Editar a {0}'.format(u,)
    subtitle = 'Información de Usuario'
    form = forms.UserRegisterForm(request.POST or None, instance=object)
    group_form = forms.GroupForm(request.POST or None, initial = {'groups': object.groups.first().id })

    if request.method == 'POST':
        if form.is_valid() and group_form.is_valid():
            update = form.save(commit=False)
            update.save()
            user_group = User.groups.through.objects.get(user=object)
            user_group.group = group_form.cleaned_data.get('groups')
            user_group.save()
            messages.add_message(request, messages.SUCCESS, 'Información Actualizada Correctamente.')
            return HttpResponseRedirect(reverse('users:view'))
        else:
            messages.add_message(request, messages.ERROR, 'Verifica tu información.')
    return render(request, 'views/profile/edit.html', locals())


#  Edit Password   #
#@permission_required('auth.change_user', login_url='users')
@login_required (login_url='login')
def password(request, pk):
    user_password = 'active'
    btn_update = 'Actualizar Contraseña'
    btn = 'Ver Perfil'
    btn_url = reverse('profile:view', kwargs={'pk':pk})
    object = get_object_or_404(User.objects.exclude(is_superuser=1), id=pk)
    u = object.username
    title = 'Editar a {0}'.format(u,)
    subtitle = 'Contraseña de Usuario'
    form = forms.UserChangePassword(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            U = User.objects.get(id__exact=pk)
            password = form.cleaned_data.get('password')
            U.set_password(password)
            U.save()
            messages.add_message(request, messages.SUCCESS, 'Información Actualizada Correctamente.')
            return HttpResponseRedirect(reverse('profile:password', kwargs={'pk':pk}))
        else:
            messages.add_message(request, messages.ERROR, 'Verifica las contraseñas.')
    return render(request, 'views/profile/edit.html', locals())


#   Edit Aditional data   #
#@permission_required('auth.change_user', login_url='users')
@login_required (login_url='login')
def data(request, pk):
    user_profile = 'active'
    btn_update = 'Actualizar Perfil'
    btn = 'Ver Perfil'
    btn_url = reverse('profile:view', kwargs={'pk':pk})
    object = get_object_or_404(User.objects.exclude(is_superuser=1), id=pk)
    u = object.username
    title = 'Editar a {0}'.format(u,)
    subtitle = 'Información personal'
    profile, created = models.Profile.objects.get_or_create(user=object)
    object = get_object_or_404(models.Profile, user_id=pk)
    form = forms.ProfileForm(request.POST or None, instance=object)
    #type_form = forms.AsesorTypeForm(request.POST or None, instance=object)
    if request.method == 'POST':
        if form.is_valid():
            update = form.save(commit=False)
            update.save()
            messages.add_message(request, messages.SUCCESS, 'Información Actualizada Correctamente.')
            return HttpResponseRedirect(reverse('profile:data', kwargs={'pk':pk}))
        else:
            messages.add_message(request, messages.ERROR, 'Verifica tu información.')
    return render(request, 'views/profile/edit.html', locals())

#   Edit Contact data   #
#@permission_required('auth.change_user', login_url='users')
@login_required (login_url='login')
def contact(request, pk):
    user_contact = 'active'
    btn_update = 'Actualizar Contacto'
    btn = 'Ver Perfil'
    btn_url = reverse('profile:view', kwargs={'pk':pk})
    object = get_object_or_404(User.objects.exclude(is_superuser=1), id=pk)
    u = object.username
    title = 'Editar a {0}'.format(u,)
    subtitle = 'Información de contacto'
    contact, created = models.Contact.objects.get_or_create(user=object)
    object = get_object_or_404(models.Contact, user_id=pk)
    form = forms.ContactForm(request.POST or None, instance=object)
    if request.method == 'POST':
        if form.is_valid():
            update = form.save(commit=False)
            update.save()
            messages.add_message(request, messages.SUCCESS, 'Información Actualizada Correctamente.')
            return HttpResponseRedirect(reverse('profile:contact', kwargs={'pk':pk}))
        else:
            messages.add_message(request, messages.ERROR, 'Verifica tu información.')
    return render(request, 'views/profile/edit.html', locals())

#   Edit Hiring data   #
#@permission_required('auth.change_user', login_url='users')
@login_required (login_url='login')
def hiring(request, pk):
    user_hiring = 'active'
    btn_update = 'Actualizar'
    btn = 'Ver Perfil'
    btn_url = reverse('profile:view', kwargs={'pk':pk})
    object = get_object_or_404(User.objects.exclude(is_superuser=1), id=pk)
    vendor = User.objects.filter(groups__name__in=['Vendedor'], id=pk).count()
    u = object.username
    title = 'Editar a {0}'.format(u,)
    subtitle = 'Información Laboral'
    hiring, created = models.Hiring.objects.get_or_create(user=object)
    object = get_object_or_404(models.Hiring, user_id=pk)
    form = forms.HiringForm(request.POST or None, instance=object)
    type_form = forms.AsesorTypeForm(request.POST or None, instance=object)
    if request.method == 'POST':
        if form.is_valid() and type_form.is_valid():
            update = form.save(commit=False)
            update.save()
            update2 = type_form.save(commit=False)
            update2.save()
            messages.add_message(request, messages.SUCCESS, 'Información Actualizada Correctamente.')
            return HttpResponseRedirect(reverse('profile:hiring', kwargs={'pk':pk}))
        else:
            messages.add_message(request, messages.ERROR, 'Verifica tu información.')
    return render(request, 'views/profile/edit.html', locals())

#   Edit Picture data   #
#@permission_required('auth.change_user', login_url='users')
@login_required (login_url='login')
def picture(request, pk):
    user_image = 'active'
    btn_update = 'Añadir imagen'
    btn = 'Ver Perfil'
    btn_url = reverse('profile:view', kwargs={'pk':pk})
    object = get_object_or_404(User.objects.exclude(is_superuser=1), id=pk)
    u = object.username
    title = 'Editar a {0}'.format(u,)
    subtitle = 'Imagen de Perfil'
    picture, created = models.Picture.objects.get_or_create(user=object)
    object = get_object_or_404(models.Picture, user_id=pk)
    form = forms.PictureForm(request.POST, request.FILES, instance=object)
    if request.method == 'POST':
        if form.is_valid():
            update = form.save(commit=False)
            update.save()
            messages.add_message(request, messages.SUCCESS, 'Imagen guardada con éxito.')
            return HttpResponseRedirect(reverse('profile:picture', kwargs={'pk':pk}))
        else:
            messages.add_message(request, messages.ERROR, 'No se pudo añadir la imagen.')
    return render(request, 'views/profile/edit.html', locals())


#   Delete Picture data   #
#@permission_required('auth.change_user', login_url='users')
@login_required (login_url='login')
def delete_picture(request, pk):
    btn_update = 'Eliminar'
    btn = 'Cancelar'
    btn_url = reverse('profile:picture', kwargs={'pk':pk})
    object = get_object_or_404(User.objects.exclude(is_superuser=1), id=pk)
    u = object.username
    title = 'Eliminar fotografía de {0}'.format(u,)
    subtitle = 'Imagen de Perfil'
    object = get_object_or_404(models.Picture.objects, user_id=pk)
    if request.method == 'POST':
        delete = object.delete()
        messages.add_message(request, messages.INFO, 'Imagen eliminada con éxito.')
        return HttpResponseRedirect(reverse('profile:picture', kwargs={'pk':pk}))
    return render(request, 'forms/delete.html', locals())
