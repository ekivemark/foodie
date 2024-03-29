#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import direct_to_template
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

    # Media and Static -  comment out for production config! -------------
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
                {'document_root': settings.MEDIA_ROOT}),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve',
                {'document_root': settings.STATIC_ROOT}),

    # Search urls ---------------------------------------------------------

    # Home url -----------------------------------------------------------

    (r'^home/$', include('foodie.apps.home.urls')),
    url(r'^mobile/info/(?P<phone_number>[^/]+)/$', 'foodie.apps.mobile.views.Show_Profile', name='profile'),
    (r'^mobile/$', include('foodie.apps.mobile.urls')),

    # App urls -----------------------------------------------------------
    #(r'^api/$', include('foodie.apps.api.urls')),
    url(r'^api/message/', 'foodie.apps.api.views.sms_messages', name="sms_messages"),
    url(r'^api/send/$', 'foodie.apps.api.views.sms_send', name='sms_send'),
    url(r'^api/incoming/$', 'foodie.apps.api.views.incoming', name='incoming'),

    url(r'^$', 'foodie.apps.home.views.home'),
    # App urls -----------------------------------------------------------
    # url(r'^api/(?P<pat_id>\S+)$', 'foodie.apps.api.urls',
    #    name='home'),
    (r'^nutrition/',  include('foodie.apps.nutrition.urls')),
    # Static Pages


    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

