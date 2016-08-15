from django.conf.urls import url

from . import views

app_name = 'auth'

urlpatterns = [
	url(r'^$',views.index,name='index'),
    url(r'^signin/$', views.signin, name='signin'),
    url(r'^signup/$',views.signup,name='signup'),
    url(r'^signout/$',views.signout,name='logout'),
    url(r'^register/$',views.register,name='register'),
]