from django.conf.urls import patterns, include, url
from django.contrib import admin
from RequestApp import views
from django.conf import settings

urlpatterns = patterns('',

    url(r'^signin/?$', views.signin),
    url(r'^/?$', views.index),
    url(r'^admin/', include(admin.site.urls)),

    url(r'^companiespage?$', views.companiespage),
    url(r'^userspage?$', views.userspage),
    url(r'^equipspage?$',views.equipspage),
    url(r'^active_requests?$', views.active_requests),

    url(r'^(?P<pk>[0-9]+)/DetailCompany$', views.DetailCompany),
    url(r'^get_name?$', views.get_name),
    url(r'^results?$', views.results),
    url(r'^new_request?$', views.new_request),
    url(r'^created_request?$', views.created_request),
    url(r'^(?P<pk>[0-9]+)/request_journal$', views.request_journal)
)

urlpatterns += patterns('',
                            url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {
                              'document_root': settings.STATIC_ROOT,
                            }),
                        )