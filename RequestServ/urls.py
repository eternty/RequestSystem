from django.conf.urls import patterns, include, url
from django.contrib import admin
from RequestApp import views
urlpatterns = patterns('',
    # Examples:
    url(r'^signin/?$', views.signin),
    url(r'^$', views.index),
    # url(r'^blog/', include('blog.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^hello$', views.hello, name= "hello"),
    url(r'^client$', views.client),
    url(r'^dispatcher$',views.dispatcher),
    url(r'^engineer$',views.engineer),
    url(r'^new_req$',views.new_req)
)
