#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns, include, url

from views import *

urlpatterns = patterns('',

    #url(r'^loaddata$', loaddata, name='loaddata'),
    url(r'^suggest$', suggest, name='suggest'),
    
)