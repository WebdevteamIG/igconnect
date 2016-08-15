from django.conf.urls import url

from . import views

app_name = 'profileSpace'

urlpatterns = [
	url(r'^view/?(?P<username>\w+)?/?$',views.index,name='index'),
	url(r'^view$',views.index,name='index'),
	url(r'^edit/$',views.edit,name='edit'),

]