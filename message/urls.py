from django.conf.urls import url

from . import views

app_name = 'message'

urlpatterns = [
	url(r'^view/?(?P<id>\w+)?/?$',views.index,name='index'),
	url(r'^view$',views.index,name='index'),
	url(r'^$',views.index,name='index'),
	url(r'^send/',views.send,name='index'),
]