__author__ = 'mark'


from django.conf import settings
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from forms import *
from utils import *


#@login_required
#@access_required("tester")
def sms_send(request):

    print "in the send"

    print request.GET
    print request.POST
    

    if request.method == 'POST':

        form = SMSSendForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "SMS Sent.")
            return render_to_response('smsreminders/send.html',
                    {'form': SMSSendForm()},
                context_instance = RequestContext(request))
            #the form has errors
        return render_to_response('smsreminders/send.html',
                {'form': form},
            context_instance = RequestContext(request))

    #request is a GET (not a POST)
    return render_to_response('smsreminders/send.html',
            {'form': SMSSendForm()},
        context_instance = RequestContext(request))


#@login_required
#@access_required("tester")
def sms_messages(request):


    print "in Messages"


    smsmessages=get_messages()
    return render_to_response('smsreminders/messages.html',
            {'smsmessages': smsmessages},
        context_instance = RequestContext(request))



def incoming(request):


    print "In incoming"

    return render_to_response('home/index.html', {
        'next':set_next,
        'server_address':request.get_host(),},
        RequestContext(request))


