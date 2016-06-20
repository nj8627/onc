from django.conf.urls import patterns, url
from d3_account import views

urlpatterns = patterns('',
		url(r'^new/$', views.index, name='home_2'),
		
)

