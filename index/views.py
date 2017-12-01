# -*- coding: utf-8 -*-
from __future__ import unicode_literals
# django decorators for login and permission purpose
from django.contrib.auth.decorators import login_required, permission_required
# django login and logout modules
from django.contrib.auth import logout, authenticate, login, get_user_model
#django required modules for send email
from django.shortcuts import get_object_or_404
from django.contrib import messages
#django render modules
from django.core.urlresolvers import reverse
from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import Context, RequestContext
from django.template.loader import get_template
#django forms such as Login and ContactForm
from . import forms
#get the static url on views url = static('x.jpg')
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.contrib.auth.models import User, Group
#Get the current site.
#current_site = Site.objects.get_current()
from datetime import datetime, timedelta
from . import models
import pytz

@login_required (login_url='index:login')
def view(request):
	return render(request, 'masters/blank.html', locals())



def log_in(request):
	if request.user.is_authenticated():
		return HttpResponseRedirect(reverse('index:view'))
	if request.method == 'POST':
		form = forms.Login_Form(request.POST or None)
		if form.is_valid():
			username = form.cleaned_data.get("username").lower()
			password = form.cleaned_data.get("password")
			user = authenticate(username=username, password=password)
			login(request, user)
			if user.first_name:
				u = user.first_name
			else:
				u = user.username
			messages.success(request, 'Bienvenido %s.'%u)
			return HttpResponseRedirect(reverse('index:view'))
		else:
			username = form.cleaned_data.get("username").lower()
			password = form.cleaned_data.get("password")
			try:
				user = User.objects.get(username=username)
				user_validated  = User_Register_Token.objects.get(user_id=user.id)
				check_pass = user.check_password(password)
				if (user_validated.status is True and user.is_active is True) and check_pass is False:
					messages.error(request, 'Verifica tus Credenciales de Acceso')
				elif (user_validated.status is True and user.is_active is False) and check_pass is True:
					messages.error(request, 'Esta cuenta se encuentra Suspendida. Ponte en contacto con Nosotros.')
				elif (user_validated.status is False and user.is_active is False) and check_pass is True:
					val = True
					messages.error(request, 'Esta cuenta de correo no ha sido activada.')
				else:
					messages.error(request, 'Verifica tus Credenciales de Acceso')
			except:
				messages.error(request, 'Error de Usuario y/o Contraseña.')
	else:
		form = forms.Login_Form()
	return render(request, 'views/index/login.html', locals())



#Función para cerrar sesión
@login_required (login_url='index:login')
def log_out(request):
	if request.user.first_name:
		u = request.user.first_name
	else:
		u = request.user.username
	logout(request)
	messages.success(request, 'Hasta luego %s.'%(u))
	return HttpResponseRedirect(reverse('index:login'))


