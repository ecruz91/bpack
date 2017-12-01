from django.conf.urls import url
from django.contrib import admin
from . import views
from django.conf.urls import handler404


urlpatterns = [
	url(r'^$', views.view, name='view'),
	url(r'^login/$', views.log_in, name='login'),
	url(r'^logout/$', views.log_out, name='logout'),
	#url(r'^404/$', views.error404, name='error404'),
]
#handler404 = views.error404
