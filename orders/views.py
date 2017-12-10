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
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import Context, RequestContext
from django.template.loader import get_template
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template import Template
from forms import OrderForm, Order_Pallet
from models import Orders, Pallets, Rolls, Drops, Drop_Number
from django.forms import inlineformset_factory
# Class based views
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView
from digg_paginator import DiggPaginator
from clients.models import Clients
from products.models import Product
import json
from django.views.decorators.csrf import csrf_exempt

#######################
#  Render all orders  #
#######################
@method_decorator(login_required(login_url='index:login'), name='dispatch')
@method_decorator(permission_required('orders.view_orders', login_url='index:view'), name='dispatch')
class view(ListView):
	model = Orders
	paginator_class = DiggPaginator
	paginate_by = 20
	template_name = 'views/orders/orders.html'

	def get_queryset(self, *args, **kwargs):
		qs = super(view, self).get_queryset(*args, **kwargs).order_by('-id')
		if self.request.user.groups.filter(name='empacador').exists():
			qs = qs.filter(packer_id= self.request.user.id)
		if 'query' in self.request.GET:
			query = self.request.GET['query']
			qs =(qs.filter(order__icontains=query)|
			qs.filter(bpid__icontains=query)|
			qs.filter(lq__icontains=query)|
			qs.filter(lq__icontains=query)|
			qs.filter(client_name__icontains=query)|
			qs.filter(packer_name__icontains=query)|
			qs.filter(product_name__icontains=query))
		return qs
	def get_context_data(self, *args, **kwargs):
		context = super(view, self).get_context_data(*args, **kwargs)
		if 'query' in self.request.GET:
			context["query"] = self.request.GET['query']
			context["subtitle"] = "Resultados de Búsqueda"
			context["btn"] = "Limpiar"
			context["btn_url"] = reverse("orders:view")
		else:
			context["subtitle"] = "Lista de Ordenes"
			context["btn"] = "Nueva Orden"
			context["btn_url"] = reverse("orders:new")
		context["results"] = self.get_queryset().count()
		context["title"] = "Ordenes"
		context["q_url"] = reverse("orders:view")
		return context

#######################################
#  Register a New Order in the system #
#######################################
#@permission_required('orders.new_orders', login_url='index:login')
@login_required(login_url='index:login')
def new(request):
	#object_list = Group.objects.all()
	title = "Nueva Orden"
	subtitle = "Agregar una nueva orden al sistema"
	page = "Formulario de registro"
	btn = "Cancelar"
	btn_url = reverse("orders:view")
	if request.method == 'POST':
		form = OrderForm(request.POST, request.FILES)
		if form.is_valid():
			f = form.save(commit=False)
			f.client_name = f.client.NAME.upper()
			f.product_name = f.product.product.upper()
			f.packer_name = f.packer.get_full_name().upper()
			f.qty = f.product.qty
			f.save()
			messages.success(request, 'Orden creada correctamente')
			return HttpResponseRedirect(reverse('orders:config', kwargs={'pk':f.id}))
		else:
			messages.error(request, 'Error al Crear la orden')
	else:
		form = OrderForm()
	return render(request, 'forms/new_order.html', locals())

##################################
#  Delete an Order in the system #
##################################
@permission_required('orders.delete_product', login_url='index:login')
@login_required (login_url='index:login')
def delete(request, pk):
	btn = 'Cancelar'
	object = get_object_or_404(Orders.objects, id=pk)

	#variable_delete = object.CONTACT_NAME_1
	subtitle = 'Eliminar Orden'
	btn_url = reverse('orders:view')
	if request.method == 'POST':
		messages.info(request, 'Se eliminó la orden %s satisfactoriamente'%(object))
		delete = object.delete()
		return HttpResponseRedirect(reverse('orders:view'))
	return render(request, "forms/delete.html", locals())


################################
#  Edit an Order in the system #
################################
@permission_required('products.change_product', login_url='index:login')
@login_required (login_url='index:login')
def edit(request, pk):
	pk = int(pk)
	u_img=True
	btn_update = 'Actualizar Orden'
	btn = 'Cancelar'
	#btn_url = reverse('orders:new')
	object = get_object_or_404(Orders.objects, id=pk)
	btn_url = reverse( 'orders:config', args=[(object.id)])
	title = 'Editar {0}'.format(object,)
	subtitle = 'Editar Ordenes'
	if request.method == 'POST':
		form = OrderForm(request.POST or None, instance=object)
		if form.is_valid():
			update = form.save(commit=True)
			update.client_name = update.client.NAME.upper()
			update.product_name = update.product.product.upper()
			update.packer_name = update.packer.get_full_name().upper()
			update.qty = update.product.qty
			update.save()
			messages.success(request, 'Se actualizó la orden %s'%(object))
			return HttpResponseRedirect(reverse( 'orders:config', args=[(object.id)]))
		else:
			messages.error(request, 'Verifica tu información')
	else:
		form = OrderForm(instance=object)
	return render(request, 'forms/new_p.html', locals())

#################################
#  Close an order in the system #
#################################
@permission_required('products.change_product', login_url='index:login')
@login_required (login_url='index:login')
def close(request, pk):
	pk = int(pk)
	object = get_object_or_404(Orders.objects, id=pk)
	object.flag = 2
	object.save()
	return HttpResponseRedirect(reverse('orders:view'))

#######################
#  Configuring Order #
######################
def config(request, pk):
	btn_update = 'Generar Cotización'
	btn = 'Ver Ordenes'
	object = get_object_or_404(Orders.objects, id=pk)
	btn_url = reverse('orders:view')
	u = object.order
	title = 'Configuración de Cotización'
	subtitle = '%s'%(u)

	return render(request, 'views/orders/config.html', locals())


##########################
#  Creating packing list #
##########################
"""
@method_decorator(login_required(login_url='index:login'), name='dispatch')
class pallets(ListView):
	paginator_class = DiggPaginator
	paginate_by = 1
	model = Pallets
	template_name = 'views/orders/pallets.html'
	def get_queryset(self, *args, **kwargs):
		qs = super(pallets, self).get_queryset(*args, **kwargs).order_by('id').filter(order_id=self.kwargs['pk'])
		return qs
	def get_context_data(self, *args, **kwargs):
		context = super(pallets, self).get_context_data(*args, **kwargs)
		try:
			context['object'] = Orders.objects.get(id=self.kwargs['pk'])
		except:
			raise Http404
		context['roll_list'] = Rolls.objects.filter(order_id=context['object'].id).order_by('roll_name')
		context['pk'] = self.kwargs['pk']
		context["btn"] = 'Cancelar'
		context["btn_url"] = reverse("orders:config", kwargs={'pk':self.kwargs['pk']})
		context["create_url"] = reverse("orders:new_pallet", kwargs={'pk':self.kwargs['pk']})
		context["q_url"] = reverse("orders:config", kwargs={'pk':self.kwargs['pk']})
		context["btn2"] = 'Nueva Tarima'
		context["btn_url2"] = reverse("orders:new_pallet", kwargs={'pk':self.kwargs['pk']})
		context["title"] = "Orden: %s - %s"%(context['object'].order, context['object'].client_name)
		context["subtitle"] = '%s'%(context['object'].product_name)
		context['objects'] = Orders.objects.filter(id=self.kwargs['pk']).order_by('-id')
		return context
"""

def pallets(request,pk):
	object = get_object_or_404(Orders.objects.filter(id=pk))
	if request.user.groups.filter(name='empacador').exists() and request.user.id != object.packer_id:
		raise Http404
	object = Pallets.objects.filter(order_id=pk).first()
	try:
		return HttpResponseRedirect(reverse("orders:view_pallet", kwargs={'pk':object.id}))
	except:
		return HttpResponseRedirect(reverse("orders:new_pallet", kwargs={'pk':pk}))
	
def view_pallet(request,pk):
	pallet = get_object_or_404(Pallets.objects.filter(id=pk))
	object = Orders.objects.get(id=pallet.order_id)
	if request.user.groups.filter(name='empacador').exists() and request.user.id != object.packer_id:
		raise Http404
	title = "Orden: %s - %s"%(object.order, object.client_name)
	subtitle = '%s - %s'%(object.product_name, object.packer.get_full_name())
	pallet_list = Pallets.objects.filter(order_id=object.id)
	drop_list = Drop_Number.objects.filter(drop__pallet_id=pallet.id)
	roll_list = Rolls.objects.filter(order_id=object.id).order_by('roll_name')
	return render(request, 'views/orders/pallets.html', locals())
##########################
#  Creating new pallet   #
##########################
@login_required (login_url='login')
def new_pallet(request, pk):
	object = get_object_or_404(Orders.objects.filter(id=pk))
	if request.user.groups.filter(name='empacador').exists() and request.user.id != object.packer_id:
		raise Http404
	count_pallets = Pallets.objects.filter(order_id=pk).count()
	last_pallet = Pallets.objects.filter(order_id=pk).last()
	if Drops.objects.filter(pallet_id=last_pallet.id).count() == 0:
		messages.error(request, 'No puedes dejar listas de empaque vacías')
		return HttpResponseRedirect(reverse("orders:pallets", kwargs={'pk':pk}))
	if count_pallets >= 10:
		messages.error(request, 'No es posible asignar más de 10 Tarimas')
		return HttpResponseRedirect(reverse("orders:pallets", kwargs={'pk':pk}))
	name = count_pallets+1
	#object = Pallets.objects.create(order=object, name=name).save()
	#pallets = Pallets.objects.create(order=object).save()
	messages.success(request, 'Tarima creada correctamente')
	return HttpResponseRedirect(reverse("orders:pallets", kwargs={'pk':pk}))
	
	

def delete_pallet(request, pk):
	object = get_object_or_404(Orders.objects.filter(id=pk))
	if request.user.groups.filter(name='empacador').exists() and request.user.id != object.order.packer_id:
		raise Http404

	if Pallets.objects.filter(order_id=pk).count() == 1:
		messages.error(request, 'La orden debe tener al menos una lista de Empaque')
		return HttpResponseRedirect(reverse('orders:pallets', kwargs={'pk':object.id}))

	object = Pallets.objects.filter(order_id=pk).last()
	if Drops.objects.filter(pallet_id=object.id).count() >=1:
		messages.error(request, 'No se puede Eliminar una Lista de Empaque Con Datos')
		return HttpResponseRedirect(reverse('orders:pallets', kwargs={'pk':object.order_id}))

	btn = 'Cancelar'
	subtitle = 'Eliminar Tarima'
	btn_url = reverse('orders:view')
	if request.method == 'POST':
		messages.info(request, 'Se eliminó la tarima %s satisfactoriamente'%(object.name))
		delete = object.delete()
		return HttpResponseRedirect(reverse('orders:pallets', kwargs={'pk':object.order_id}))
	return render(request, "forms/delete.html", locals())


def ajax_response(request):
	if request.method == 'POST':
		nid = request.POST.get('nid','')
		results = []
		object_list = Clients.objects.filter(product__id=nid).order_by('NAME')
		for object in object_list:
			print object.id
			result = {"id":object.id, "name":object.NAME}
			results.append(result)
		return HttpResponse(json.dumps({'results': results}, indent=3), content_type="application/json")
	else:
		raise Http404



#Impresion de Listas de Empaque

#@permission_required('products.delete_product', login_url='index:login')
@login_required (login_url='index:login')
def printing(request, pk):
	if request.user.groups.filter(name='empacador').exists() and request.user.id != object.order.packer_id:
		raise Http404
	btn = 'Cancelar'
	object = get_object_or_404(Orders.objects, id=pk)
	object_list = Pallets.objects.filter(order_id = pk)
	#variable_delete = object.CONTACT_NAME_1
	subtitle = 'Eliminar Contacto del Cliente'
	btn_url = reverse( 'orders:config', args=[(object.id)])
	return render(request, "views/orders/print.html", locals())


#Agregar Rollo al Sistema
#@permission_required('products.delete_product', login_url='index:login')
@login_required (login_url='index:login')
def add_roll(request):
	if request.method == 'POST':
		nid = request.POST.get('primarykey','')
		val = request.POST.get('roll_name','')[:2]
		print nid
		object = get_object_or_404(Orders.objects, id=nid)
		if request.user.groups.filter(name='empacador').exists() and request.user.id != object.order.packer_id:
			raise Http404

		if Rolls.objects.filter(order_id=object.id).count() >= 15:
			messages.error(request, 'No es posible crear Más de 15 Rollos')
			return HttpResponseRedirect(reverse('orders:pallets', kwargs={'pk':nid}))

		try:
			roll = Rolls(order_id=object.id, roll_name=val)
			roll.save()
			
			messages.success(request, 'Rollo %s Creado con Satisfacción'%(val))
			return HttpResponseRedirect(reverse('orders:pallets', kwargs={'pk':object.id}))
		except:
			messages.error(request, 'No es posible crear el rollo %s'%(val))
			return HttpResponseRedirect(reverse('orders:pallets', kwargs={'pk':nid}))
	else:
		raise Http404



##################################
#  Delete an Order in the system #
##################################
@permission_required('orders.delete_product', login_url='index:login')
@login_required (login_url='index:login')
def delete_roll(request, pk):
	btn = 'Cancelar'
	object = get_object_or_404(Rolls.objects, id=pk)
	subtitle = 'Eliminar Rollo'
	btn_url = reverse('orders:pallets', kwargs={'pk':object.order_id})
	if request.method == 'POST':
		messages.info(request, 'Se eliminó el Rollo %s satisfactoriamente'%(object))
		delete = object.delete()
		return HttpResponseRedirect(btn_url)
	return render(request, "forms/delete.html", locals())


##############################################
#  Add Serie an Multiple Downs in the system #
##############################################

@login_required (login_url='index:login')
def add_drops(request):
	if request.method == 'POST':
		primarykey = request.POST.get('primarykey','')
		dropkey = request.POST.get('dropkey','')
		total_weight = round(float(request.POST.get('total_weight','')),2)
		drops_loop = int(request.POST.get('drops_loop',''))
		serie = request.POST.get('serie','')[:1]
		pallet = request.POST.get('pallet')
		object = get_object_or_404(Orders.objects, id=primarykey)
		if request.user.groups.filter(name='empacador').exists() and request.user.id != object.order.packer_id:
			raise Http404
		###Validar que Las tarimas y las Bajadas pertenezcan a las llaves insertadas
		#object = get_object_or_404(Pallets.objects, id=pallet)
		#object = get_object_or_404(Drops.objects, id=dropkey)

		delta = round(float(total_weight/drops_loop),2)
		#logica para agregar forloops
		
		drops = Drops(pallet_id=pallet, roll_id=dropkey, serie=serie)
		drops.save()
		for x in range(0,drops_loop):
			alpha = x+1
			drop = Drop_Number(drop_id=drops.id, weight=delta, drop_name = alpha)
			drop.save()
		drops.save()
		messages.success(request, 'Bajadas Creadas con Satisfacción')
		return HttpResponseRedirect(reverse('orders:pallets', kwargs={'pk':primarykey}))
		"""
		except:
			messages.error(request, 'No es posible crear tantas bajadas')
			return HttpResponseRedirect(reverse('orders:pallets', kwargs={'pk':primarykey}))
		"""
		"""
		try:
			roll = Rolls(order_id=object.id, roll_name=val)
			roll.save()
			
			messages.success(request, 'Rollo %s Creado con Satisfacción'%(val))
			return HttpResponseRedirect(reverse('orders:pallets', kwargs={'pk':object.id}))
		except:
			messages.error(request, 'No es posible crear el rollo %s'%(val))
			return HttpResponseRedirect(reverse('orders:pallets', kwargs={'pk':nid}))
		"""
	else:
		raise Http404



##################################################
#  Delete a Drop and Drops_numbers in the system #
##################################################
@login_required (login_url='index:login')
def delete_drops(request, pk):
	btn = 'Cancelar'
	object = get_object_or_404(Drops.objects, id=pk)
	subtitle = 'Eliminar Bajada'
	btn_url = reverse('orders:pallets', kwargs={'pk':object.pallet.order_id})
	if request.method == 'POST':
		messages.info(request, 'Se eliminó el Rollo %s satisfactoriamente'%(object))
		delete = object.delete()
		return HttpResponseRedirect(btn_url)
	return render(request, "forms/delete.html", locals())



###################################
#  Edit Drop-Number in the system #
###################################
@csrf_exempt
@login_required (login_url='index:login')
def edit_drop(request):
	if request.method == 'POST':
		pk=request.POST.get('pk')
		value = request.POST.get('value','')
		name = request.POST.get('name','')
		object = Drop_Number.objects.get(id=pk)
		object.weight = value
		object.save()
	return render(request, "forms/delete.html", locals())


###################################
#  Edit Drop-Number in the system #
###################################
@login_required (login_url='index:login')
def edit_drops(request,pk):
	pk=pk
	object_list = Drop_Number.objects.filter(drop_id=pk)

	
	return render(request, "views/orders/includes/edit_drops.html", locals())