from django.views.generic import TemplateView
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.view.as_view(), name='view'),
    url(r'^new/$', views.new, name='new'),
    url(r'^delete/@(?P<pk>\d+)/$', views.delete, name='delete'),
    url(r'^edit/@(?P<pk>\d+)/$', views.edit, name='edit'),


    url(r'^printing/@(?P<pk>\d+)/$', views.printing, name='printing'),
    url(r'^close/@(?P<pk>\d+)/$', views.close, name='close'),
    url(r'^config/@(?P<pk>\d+)/$', views.config, name='config'),
    url(r'^config/pallets/@(?P<pk>\d+)/$',views.pallets, name='pallets'),

    url(r'^config/view/@(?P<pk>\d+)/$', views.view_pallet, name='view_pallet'),
    
    url(r'^config/pallets/new/@(?P<pk>\d+)/$',views.new_pallet, name='new_pallet'),
    url(r'^config/pallets/delete/@(?P<pk>\d+)/$', views.delete_pallet, name='delete_pallet'),
    url(r'^ajax_response/$', views.ajax_response, name='ajax_response'),

    #Proceso de Calculo de Subidas y Bajadas
    url(r'^add_roll/$', views.add_roll, name='add_roll'),
    url(r'^delete_roll/@(?P<pk>\d+)/$', views.delete_roll, name='delete_roll'),

    url(r'^add_drops/$', views.add_drops, name='add_drops'),
    url(r'^delete_drops/@(?P<pk>\d+)/$', views.delete_drops, name='delete_drops'),
    url(r'^edit_drop/$', views.edit_drop, name='edit_drop'),


    url(r'^edit_drops/@(?P<pk>\d+)/$', views.edit_drops, name='edit_drops'),
]

