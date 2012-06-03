#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import direct_to_template
from views import *

urlpatterns = patterns('',

    url(r'^$', home, name='home'),
    url(r'^test$', test, name='test'),
    
)