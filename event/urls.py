

from django.conf.urls import url

from . import views

app_name = 'event'

urlpatterns = [
	url(r'^$',views.index,name='index'),
    url(r'^addEvent/$', views.addEvent, name='addEvent'),
    url(r'^viewall/$',views.viewall,name='viewall'),
    url(r'^viewall/(?P<pageNo>\d+)/$',views.viewall,name='viewall'),
]
