from django.views.generic import TemplateView
from django.conf.urls import url
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^$', views.list_clients.as_view(), name='view'),

    url(r'^new/$', views.new_clients, name='new'),
    url(r'^delete/@(?P<pk>\d+)/$', views.delete_client.as_view(), name='delete'),

    url(r'^edit/contact/@(?P<pk>\d+)/$', views.contact, name='contact'),
    url(r'^new/contact/@(?P<pk>\d+)/$', views.new_contact, name='add_contact'),
    url(r'^edit/contacts/@(?P<pk>\d+)/$', views.contacts, name='edit_contact'),
    url(r'^delete/contacts/@(?P<pk>\d+)/$', views.delete_contacts, name='delete_contact'),

    url(r'^profile/@(?P<pk>\d+)/$', views.profile_clients, name='profile'),
    url(r'^edit/@(?P<pk>\d+)/$', views.edit_client, name='edit'),
    
]

