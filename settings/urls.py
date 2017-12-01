# -*- coding: utf-8 -*-
from django.conf.urls import include, url
from django.contrib import admin
urlpatterns = [
	url(r'^', include('index.urls', namespace='index')),
	url(r'^users/', include('users.urls', namespace='users')),
	url(r'^profile/', include('profile.urls', namespace='profile')),
	url(r'^groups/', include('groups.urls', namespace='groups')),
	url(r'^clients/', include('clients.urls', namespace='clients')),
	url(r'^products/', include('products.urls', namespace='products')),
	url(r'^orders/', include('orders.urls', namespace='orders')),
	#url(r'^payments/', include('ecommerce.urls', namespace='ecommerce')),
]
