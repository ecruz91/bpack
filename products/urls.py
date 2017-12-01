from django.views.generic import TemplateView
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.view.as_view(), name='view'),
    url(r'^new/$', views.new, name='new'),
    url(r'^delete/@(?P<pk>\d+)/$', views.delete, name='delete'),
    url(r'^edit/@(?P<pk>\d+)/$', views.edit, name='edit'),
    url(r'^ajax_response/$', views.ajax_response, name='ajax_response'),
]
