#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu


from django.conf import settings
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

def home(request):
    try:
        set_next = request.GET['next']

    except:
        print "NO next in GET"
        set_next = "/"

    print set_next


    return render_to_response('home/index.html', {
        'next':set_next,
        'server_address':request.get_host(),},
                              RequestContext(request))



def test(request):
    set_next ="/"

    try:
        set_next = request.GET['next']

    except:
        print "NO next in GET"
        set_next = "/"

    print set_next

    context = {
               'next':set_next,
               'server_address':request.get_host(),
               }
    return render_to_response('home/test.html', context,
        RequestContext(request))
