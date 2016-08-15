from django.conf.urls import url
from . import views

app_name = 'dashboard'

urlpatterns = [
	url(r'^$',views.index,name='index'),
	url(r'^(?P<pageNo>\d+)$',views.index,name='paginationUrl'),
    url(r'^addProject/$', views.addProject, name='addProject'),
    url(r'^viewProject/$', views.viewProject, name='viewProject'),
    url(r'^updateProject/$', views.updateProject, name='updateProject'),
    url(r'^uploadFiles/$', views.uploadFiles, name='uploadFiles'),
    url(r'^deleteDocument/$', views.deleteDocument, name='deleteDocument'),
    url(r'^rate/$', views.rate, name='rate'),
	#url(r'^passProjectId/$', views.passProjectId, name='passProjectId'),
	
]