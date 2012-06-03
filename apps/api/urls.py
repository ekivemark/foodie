#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import direct_to_template
from django.conf import settings
from views import *
from utils import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

    # Search urls ---------------------------------------------------------



    # App urls -----------------------------------------------------------
    url(r'^incoming/$',incoming,
        name='incoming'),

    url(r'^send/$', sms_send, name='sms_send'),
    url(r'^messages/$', sms_messages, name='sms_messages'),

    # Static Pages


    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)

