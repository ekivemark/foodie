#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import direct_to_template
from views import *
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

    url(r'^record/(?P<phone_number>[^/]+)/$', Show_Profile, name='profile'),
    url(r'^history/(?P<phone_number>[^/]+)/$', history, name='history'),
    url(r'^$', Show_Profile , name='profile'),
    
)