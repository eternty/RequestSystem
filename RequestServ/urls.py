from django.conf.urls import patterns, include, url
from django.contrib import admin
from RequestApp import views
from django.conf import settings

urlpatterns = patterns('',

    url(r'^signin/?$', views.signin),
    url(r'^$', views.index),

    url(r'^admin/', include(admin.site.urls)),



)

urlpatterns += patterns('',
                            url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {
                              'document_root': settings.STATIC_ROOT,
                            }),
                        )