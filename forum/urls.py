from django.conf.urls import url

from . import views

app_name = 'forum'

urlpatterns = [
	url(r'^$',views.viewAllThreads,name='viewThreads'),
	url(r'^viewThread/$', views.viewThread, name='viewThread'),
	#url(r'^threads/$',views.viewThreads,name='view'),
	url(r'^new/$',views.createThread,name='createThread'),

]