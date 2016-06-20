from django.conf.urls import patterns, url
from acc_h import views

urlpatterns = patterns('',
		url(r'^new/$', views.part_2, name='home_2'),
		url(r'^new/(?P<mkt_id>\w+)/$', views.part_1, name='home_3'),
		url(r'^new/(?P<chnl_id>\d+)/(?P<brand_id>\d+)/$', views.part_1, name='home_3'),
		url(r'^new/(?P<mkt_id>\d+)/(?P<chnl_id>\d+)/(?P<brand_id>\d+)/(?P<metric>\d+)/(?P<time_period>\d+)/(?P<blnk>\d+)/$', views.part_1, name='home_3'),
		url(r'^child_ajax/(?P<mkt_id>\d+)/(?P<chnl_id>\d+)/(?P<brand_id>\d+)/(?P<metric>\d+)/(?P<time_period>\d+)/(?P<chnl_nm>\d+)/(?P<acc_id>\d+)/(?P<blnk>\d+)/$', views.child_ajax, name='child_ajax'),
		url(r'^brand_ajax/(?P<mkt_id>\d+)/$', views.brand_ajax, name='brand_ajax'),
)

