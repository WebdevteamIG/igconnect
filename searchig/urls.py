from django.conf.urls import url

from . import views

app_name = 'searchig'

urlpatterns = [
	url(r'^$',views.index,name='index'),
	url(r'^query/(?P<searchWords>[\w|\W]+)/$',views.query,name='query'),
	url(r'^fromDash/$',views.fromDash,name='queryFromDash'),
]