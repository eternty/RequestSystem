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
    url(r'^new_request/?$', views.new_request),
    url(r'^created_request/?$', views.created_request),
    url(r'^(?P<pk>[0-9]+)/request_journal/?$', views.request_journal),
    url(r'^(?P<pk>[0-9]+)/add_comment/?$', views.add_comment),
    url(r'^(?P<pk>[0-9]+)/client_add_comment/?$', views.client_add_comment),
    url(r'^(?P<pk>[0-9]+)/user/?$',views.user),
    url(r'^engineers_by_group/?$', views.get_engineers_by_group),
    url(r'^(?P<pk>[0-9]+)/equipment/?$', views.equipment),

    url(r'^/normative_time/?$', views.normative_time),
    url(r'^(?P<pk>[0-9]+)/get_equipment/?$', views.get_equipment),
    url(r'^logout/?$', views.logout_view),
    url(r'^(?P<pk>[0-9]+)/client_request_journal/?$', views.client_request_journal)
)

urlpatterns += patterns('',
                            url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {
                              'document_root': settings.STATIC_ROOT,
                            }),
                        )