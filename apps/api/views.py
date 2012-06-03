__author__ = 'mark'


from django.conf import settings
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext



def incoming(request):


    print "In incoming"

    return render_to_response('home/index.html', {
        'next':set_next,
        'server_address':request.get_host(),},
        RequestContext(request))


