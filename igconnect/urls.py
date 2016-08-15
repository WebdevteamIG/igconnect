from django.conf.urls import patterns, include, url
import auth.views
from django.conf import settings
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'igconnect.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^auth/',include('auth.urls',namespace='auth')),
    url(r'^$', auth.views.index),
    url(r'^forum/',include('forum.urls',namespace='forum')),
    url(r'^dashboard/',include('dashboard.urls',namespace='dashboard')),
    url(r'^message/',include('message.urls',namespace='message')),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT}),
    url(r'^profile/',include('profileSpace.urls',namespace='profile')),
    url(r'^search/',include('searchig.urls',namespace='searchig')),
)
