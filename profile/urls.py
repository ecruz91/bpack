from django.views.generic import TemplateView
from django.conf.urls import url, include
from django.contrib import admin
from . import views

urlpatterns = [
	url(r'^@(?P<pk>\d+)/$', views.view, name='view'),
	#  Edit the user credentials
	url(r'^edit/@(?P<pk>\d+)/$', views.edit, name='edit'),
	#  Edit the profile models, we didn't add the prefix edit_'view' to made the reverse shorter
	url(r'^edit/data/@(?P<pk>\d+)/$', views.data, name='data'),
	url(r'^edit/password/@(?P<pk>\d+)/$', views.password, name='password'),
	url(r'^edit/picture/@(?P<pk>\d+)/$', views.picture, name='picture'),
	url(r'^edit/contact/@(?P<pk>\d+)/$', views.contact, name='contact'),
	url(r'^edit/hiring/@(?P<pk>\d+)/$', views.hiring, name='hiring'),
	#  Url to delete the picture associated with the user
	url(r'^delete/picture/@(?P<pk>\d+)/$', views.delete_picture, name='delete_picture'),
]