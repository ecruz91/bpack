from django.views.generic import TemplateView
from django.conf.urls import url, include
from django.contrib import admin
from . import views

urlpatterns = [
 	url(r'^$',views.view.as_view(), name='view'),
 	#url(r'^search/$', views.query, name='query'),
 	url(r'^new/$', views.new, name='new'),
 	url(r'^delete/@(?P<pk>\d+)/$', views.delete, name='delete'),
 	url(r'^suspend/@(?P<pk>\d+)/$', views.suspend, name='suspend'),
]