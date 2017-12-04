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
    url(r'^config/pallets/@(?P<pk>\d+)/$',views.pallets.as_view(), name='pallets'),
    url(r'^config/pallets/new/@(?P<pk>\d+)/$',views.new_pallet, name='new_pallet'),
    url(r'^config/pallets/delete/@(?P<pk>\d+)/$', views.delete_pallet, name='delete_pallet'),
    url(r'^ajax_response/$', views.ajax_response, name='ajax_response'),
]
